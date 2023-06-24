import datetime as dt

from booktech.db import initialize
from booktech.db.connection import get_db_connection
from booktech.internal.app import app
from booktech.internal.model import LiveData
from booktech.utils.logger import log


@app.task
def init_db():
    """initializes the database and populates data from files to tables"""
    initialize.init()


@app.task
def load_all(fetchsize: int=1000):
    """Load all available entries in live price table for processing

    Args:
        fetchsize: Limits the number of results to fetch
    """

    log.info(f"[Load task]: Fetching {fetchsize} records for processing")
    # Get db connection
    conn, cur = get_db_connection()

    # Fetch all live prices
    sql = "SELECT * FROM live_price"
    cur.execute(sql)
    res = cur.fetchmany(fetchsize)

    cur.close()
    conn.close()

    # Register each row as a task
    for item in res:
        data = LiveData(
            id=item[0],
            uuid=item[1],
            price=item[2],
            currency=item[3],
            last_seen=item[4],
        )

        try:
            # Only register those opportunity which have a price
            if data.price > 0:
                process(data)

            archive(data)
            delete(data)
        except Exception as err:
            log.error(f"Unable to process opportunity ID:{data.id} ,"
                      f"Error: {err}")

    log.info("[Load task]: Done")


@app.task
def process(live_data: LiveData):
    """Processes one live price opportunity

    Args:
        live_data: The live price entry to be processed
    """

    log.info(f"[Process task]: Processing record with uuid:"
             f"{live_data.uuid.hex}")
    # Get db connection
    conn, cur = get_db_connection()

    # NOTE:
    # Write the logic to check cache since we already have redis
    sql = """
    SELECT max_price FROM max_price
    WHERE uuid=%s
    """
    cur.execute(sql, (live_data.uuid.hex,))
    res = cur.fetchone()

    if not res:
        # Couldn't find any results.
        return

    max_price =  float(res[0])
    if live_data.price > max_price:
        return

    # Found a possible opportunity
    log.info(f"[Process task]: Found one opportunity - "
             f"max: {float(res[0])}, live: {live_data.price}")

    sql = """
    INSERT INTO app_output (uuid, max_price, live_price, created_at)
    VALUES (%s, %s, %s, %s);
    """
    cur.execute(sql, (
        live_data.uuid.hex,
        max_price,
        live_data.price,
        dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    cur.close()
    conn.close()
    log.info("[Process task]: Finished - created one opportunity")


@app.task
def archive(live_data: LiveData):
    """Archives one live price opportunity

    Args:
        live_data: The live price entry to be archived.
    """

    log.info(f"[Archive task]: Initiating archival process for ID={live_data.id}")
    # Get db connection
    conn, cur = get_db_connection()

    sql = """
    INSERT INTO live_price_archive (uuid, price, currency, last_seen)
    VALUES (%s, %s, %s, %s);
    """
    cur.execute(sql, (
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
def delete(live_data: LiveData):
    """Deletes entry from live price table

    Args:
        live_data: The live price entry to be deleted
    """

    log.info(f"[Delete task]: Deleting record with ID={live_data.id}")
    # Get db connection
    conn, cur = get_db_connection()

    sql = """
    DELETE FROM live_price WHERE id = %s;
    """
    cur.execute(sql, (
        live_data.id,
    ))

    conn.commit()
    cur.close()
    conn.close()
    log.info("[Delete task]: Done")
