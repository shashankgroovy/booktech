# Errors

Booktech is quite robust but you may encounter some or none of these errors or
unexpected behaviours. And when you do, then you can always refer here.

## Docker compose stopped

There can be a plethora of reasons, but if the compose setup automatically
receied a `Warm shut down requested` or a worker `excited with code 137`,
then compose must have ran out of memory.

> Docker exit code 137 implies Docker doesn't have enough RAM to finish the work.


## Common error

A common error one might see in the logs is when you spin up the application.
Here's an excerpt from it

```
ooktech-worker-2  | [2023-06-24 22:15:39,084: ERROR/ForkPoolWorker-1] Task booktech.internal.tasks.load_all[5dee3ec3-9554-476b-9eb2-58a3d803d4a0] raised unexpected: UndefinedTable('relation "live_price" does not exist\nLINE 1: SELECT * FROM live_price\n                      ^\n')
booktech-worker-2  | Traceback (most recent call last):
booktech-worker-2  |   File "/usr/local/lib/python3.10/site-packages/celery/app/trace.py", line 477, in trace_task
booktech-worker-2  |     R = retval = fun(*args, **kwargs)
booktech-worker-2  |   File "/usr/local/lib/python3.10/site-packages/celery/app/trace.py", line 760, in __protected_call__
booktech-worker-2  |     return self.run(*args, **kwargs)
booktech-worker-2  |   File "/app/booktech/internal/tasks.py", line 41, in load_all
booktech-worker-2  |     cur.execute(sql)
booktech-worker-2  | psycopg2.errors.UndefinedTable: relation "live_price" does not exist
booktech-worker-2  | LINE 1: SELECT * FROM live_price
```

This is normal and may happen in the beginning when you start.
It happens because the `load_all` task ran moments before the `init_db` task
and the table creation task hasn't finished yet.
