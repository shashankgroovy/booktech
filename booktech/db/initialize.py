import datetime as dt
import pandas as pd
from psycopg2 import DatabaseError

from booktech.utils.logger import log
from booktech.db import connection, sql


def create_tables():
    """Initializes the tables in database."""

    log.info("Creating tables")
    try:
        conn, cur = connection.get_db_connection()

        # Load the UUID extension
        cur.execute(sql.EXTENSION_UUID_DDL)

        # Create the tables
        cur.execute(sql.TABLE_MAX_PRICE_NAME)
        cur.execute(sql.TABLE_APP_OUTPUT_NAME)
        cur.execute(sql.TABLE_LIVE_PRICE_NAME)
        cur.execute(sql.TABLE_LIVE_PRICE_ARCHIVE_NAME)

        conn.commit()
        cur.close()
        conn.close()

    except DatabaseError as err:
        log.error(f"Whoops something went wrong - {err}")


def load_live_data(file: str):
    """Transforms and loads live data to DB.

    Args:
        file: str, Location or the file path to load live data from
    """
    log.info("Loading data in live_price table")
    df_live = pd.read_csv(file)

    # Fill the missing values with corresponding defaults
    df_live["price"] = df_live.price.fillna(0.0)
    df_live["currency"] = df_live.currency.fillna("")
    df_live["last_seen"] = df_live.price.fillna(dt.datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))

    # Let's store the index as ID in DB
    # This will help us for faster purge operations.
    df_live.rename_axis("id", inplace=True)

    # Time to store things in the database
    engine = connection.get_db_engine()
    df_live.to_sql(sql.TABLE_LIVE_PRICE_NAME, engine, if_exists="append")


def load_from_csv(file: str, table: str, sep: str = ","):
    """
    Loads data from csv to table

    Args:
        file: File path of the file to load the data from.
        table: Name of the table to load the data into.
        sep: File separator used in the file
    """
    log.info(f"Loading data in {table} table")
    try:
        conn, cur = connection.get_db_connection()
        cur.copy_from(file, table, sep)

        cur.close()
        conn.close()

    except DatabaseError as err:
        log.error(f"Whoops something went wrong - {err}")


def init():
    """Initializes the tables and populates the data"""

    log.info("Initializing database")

    create_tables()
    load_from_csv("data/goods_max_price.csv", sql.TABLE_MAX_PRICE_NAME)
    load_live_data("data/live_prices.csv")

    log.info("Done")
