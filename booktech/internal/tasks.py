import datetime as dt
import typing as t

import pandas as pd

from booktech.celery import app
from booktech.db import initialize, sql
from booktech.db.connection import get_db_connection, get_db_engine
from booktech.internal.model import LiveData
from booktech.utils.cache import cache
from booktech.utils.logger import log


def validate_opportunity(live_price: float, max_price: float) -> bool:
    """Core Logic:
    Returns True if live_price is greater than max_price for now.

    This function implements the core logic which may change or expand in
    future to accomodate different use cases.
    """
    return live_price > max_price


@app.task
def init_db():
    """initializes the database and populates data from files to tables"""
    initialize.init()


@app.task
def load_all(fetchsize: int=1000):
    """Load all available entries in live price table for processing

    Args:
        fetchsize: Defines the number of results to fetch in one go.
    """

    log.info(f"[Load task]: Fetching {fetchsize} records for processing")
    # Get db connection
    conn, cur = get_db_connection()

    # Fetch all live prices
    load_sql = "SELECT * FROM live_price"
    cur.execute(load_sql)
    res = cur.fetchmany(fetchsize)

    cur.close()
    conn.close()

    # Register each row as a celery task
    for item in res:
        data = LiveData(
            id=item[0],
            uuid=item[1],
            price=item[2],
            currency=item[3],
            last_seen=item[4],
        ).dict()

        try:
            # Only register those opportunity which have a price
            if data["price"] > 0:
                process.delay(data)

            # Send the opportunity for archival and deletion
            archive.delay(data)
            delete.delay(data)

        except Exception as err:
            log.error(f"Unable to process opportunity ID:{data['id']} ,"
                      f"Error: {err}")

    log.info("[Load task]: Done")


@app.task
def process(data: dict):
    """Processes one live price opportunity

    Args:
        data: dict, The live price entry to be processed
    """
    live_data = LiveData(**data)

    log.info(f"[Process task]: Processing record with uuid:"
             f"{live_data.uuid.hex}")

    # Cache check
    max_price = float(cache.get(live_data.uuid.hex) or 0)

    if not max_price:
        # Get DB connection
        _, cur = get_db_connection()

        # Cache miss! Need to get the value from database
        max_sql = """
        SELECT max_price FROM max_price
        WHERE uuid=%s
        """
        cur.execute(max_sql, (live_data.uuid.hex,))
        res = cur.fetchone()

        if not res:
            # Couldn't find any results.
            return

        max_price =  float(res[0])

        # Populate cache
        cache.set(live_data.uuid.hex, max_price)

    ok:bool = validate_opportunity(live_data.price, max_price)
    if not ok:
        return

    # It's a valid opportunity, let's save it!
    save(live_data, max_price)
    log.info("[Process task]: Finished - created one opportunity")


def save(live_data: LiveData, max_price: float):
    """Persists a new opportunity to database

    Args:
        live_data: Live data of the selected opportunity
        max_price: Max price available
    """

    log.info(f"[Process task]: Found one opportunity - "
             f"max: {max_price}, live: {live_data.price}")

    # Get DB connection
    conn, cur = get_db_connection()

    # Found a possible opportunity
    save_sql = """
    INSERT INTO app_output (uuid, max_price, live_price, created_at)
    VALUES (%s, %s, %s, %s);
    """
    cur.execute(save_sql, (
        live_data.uuid.hex,
        max_price,
        live_data.price,
        dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    cur.close()
    conn.close()


@app.task
def archive(data: dict):
    """Archives one live price opportunity

    Args:
        data: dict, The live price entry to be archived.
    """
    live_data = LiveData(**data)

    log.info(f"[Archive task]: Initiating archival process for ID={live_data.id}")
    # Get db connection
    conn, cur = get_db_connection()

    archive_sql = """
    INSERT INTO live_price_archive (uuid, price, currency, last_seen)
    VALUES (%s, %s, %s, %s);
    """
    cur.execute(archive_sql, (
        live_data.uuid.hex,
        live_data.price,
        live_data.currency,
        live_data.last_seen.strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    cur.close()
    conn.close()
    log.info("[Archive task]: Done")


@app.task
def delete(data: dict):
    """Deletes entry from live price table

    Args:
        data: dict, The live price entry to be deleted
    """
    live_data = LiveData(**data)

    log.info(f"[Delete task]: Deleting record with ID={live_data.id}")
    # Get db connection
    conn, cur = get_db_connection()

    delete_sql = """
    DELETE FROM live_price WHERE id = %s;
    """
    cur.execute(delete_sql, (
        live_data.id,
    ))

    conn.commit()
    cur.close()
    conn.close()
    log.info("[Delete task]: Done")


@app.task
def app_output_dump(filepath: t.Optional[str]=None):
    """Takes a dump of the app_output table and writes that to csv file"""

    log.info(f"[Output dump task]: Initializing dump for generated app_output data")

    # Get db engine
    engine = get_db_engine()
    df = pd.read_sql(sql.TABLE_APP_OUTPUT_NAME, engine)

    if not filepath:
        filepath = "data/app_output.csv"

    df.to_csv(filepath, index=False)
    log.info(f"[Output dump task]: Finished creating {filepath} file with generated app output data")
