import datetime as dt

from booktech.db.connection import get_db_connection
from booktech.internal.app import app
from booktech.internal.model import LiveData


@app.task
def load_live(fetchsize=1000):
    """Load all available entries in live price for processing."""

    print('Loading fresh data')
    # Get db connection
    conn, cur = get_db_connection()

    # Fetch all live prices
    live_task_sql = "SELECT * FROM live_price"
    cur.execute(live_task_sql)
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

        # Only register those opportunity which have a price
        if data.price > 0:
            process(data)

        archive(data)
        delete(data)


@app.task
def process(live_data: LiveData):
    """Processes one live price opportunity"""

    # Get db connection
    conn, cur = get_db_connection()

    # NOTE:
    # Write the logic to check cache since we already have redis
    sql = "SELECT max_price FROM max_price WHERE uuid=%s"
    cur.execute(sql, (live_data.uuid.hex,))
    res = cur.fetchone()

    if not res:
        # Couldn't find any results.
        return

    max_price =  float(res[0])
    if live_data.price > max_price:
        return

    # Found a possible opportunity
    print('Found one opportunity')
    print(f'max: {float(res[0])}, live: {live_data.price}')


    sql = """
    INSERT INTO app_output (uuid, max_price, live_price, created_at)
    VALUES (%s, %s, %s, %s);
    """
    cur.execute(sql, (
        live_data.uuid.hex,
        max_price,
        live_data.price,
        dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))

    conn.commit()
    cur.close()
    conn.close()
    print('Created an opportunity:', live_data)


@app.task
def archive(live_data: LiveData):
    """Archives one live price opportunity"""

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
        live_data.last_seen.strftime('%Y-%m-%d %H:%M:%S')
    ))

    conn.commit()
    cur.close()
    conn.close()
    print('Archived:', live_data)


@app.task
def delete(live_data: LiveData):
    """Deletes entry from live price table"""

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
    print('Deleted:', live_data)
