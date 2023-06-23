import psycopg2
from psycopg2 import extensions
from sqlalchemy import create_engine

from booktech.utils import configurator as cfg


def get_db_connection() -> tuple[extensions.connection, extensions.cursor]:
    """Returns a databse conection and cursor

    Returns:
        psycopg2 connection
        psycopg2 cursor 
    """

    config = cfg.load_yaml_config()
    conn, cur = None, None
    try:
        conn = psycopg2.connect(
            database=config["database"]["name"],
            user=config["database"]["user"],
            password=config["database"]["password"],
            host=config["database"]["host"],
            port=config["database"]["port"]
        )
        cur = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as err:
        print(f"Whoops! Error establishing connection - {err}")
        raise err

    return (conn, cur)


def get_db_engine():
    """Returns a sqlalchemy engine for connecting to the DB"""

    config = cfg.load_yaml_config()
    engine = create_engine(config["database"]["uri"])
    return engine
