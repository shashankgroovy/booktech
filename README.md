# BookTech

It's a simple application that compares prices b/w goods.
It also showcases the use of celery for scheduling task and offloading heavy work.

Here's a problem statement k


## Technical docs:

- [Installation and running the application](./docs/project-setup.md)
- [Directory Structure](./docs/directory-structure.md)
- [Architecture](./docs/architecture.md)
- [Errors](./docs/errors.md)


## Quickstart

The entire app is dockerized which makes it fairly easy to work with. Use the
following script to spin up the application.

```bash
bash bin/launch.sh
```

For more, read the [project setup guide](./docs/project-setup.md).

## Style Guide

Follow the [Python style guide - PEP 8](https://www.python.org/dev/peps/pep-0008/)
and use [Black](https://pypi.org/project/black/) as the code formatter.

## Contributing

Just hack away and happy programming!

## Working with the Database

Setting up the database is fairly easy. We can choose any SQL database and for
this we'll choose PostgreSQL.

Make sure you are in the correct directory.

1. Initialize the database with default configurations.
```
docker pull postgres
```

2. Run postgres container in docker
```
docker run --env-file=.env -p $DB_HOST_PORT:$DB_REMOTE_PORT -v $DB_MOUNT_VOLUME:$PGDATA postgres:latest
```

3. Connect to postgres via psql
The password is available as an environment variable `PGPASSWORD` in the `.env`
file. The `psql` command will automatically authenticate using that else it'll prompt for a password
```
psql -h 127.0.0.1 -p $DB_HOST_PORT -d $POSTGRES_DB -U $POSTGRES_USER
```


# Initialize the database

```
celery -A booktech call booktech.internal.tasks.init_db
```

# Spin up the worker

```
celery -A booktech worker --loglevel=INFO
```

# Start the beat!

```
celery -A booktech beat --loglevel=INFO
```

# Watch it!

```
celery -A booktech flower --loglevel=INFO
```
