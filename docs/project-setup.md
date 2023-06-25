# Project setup guide

## Requirements

- Python 3.9+
- PostgreSQL
- Redis
- Docker
- Docker Compose

## Installation

Install all the required dependencies in a virtual environment which are present
in the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Running the application

There are multiple ways to run the application which are listed below.

**Check the [Errors](./errors.md) section if you are stuck.**

> NOTE: All the environment variables are available in the `config` folder.

1. ### Using the local launch script

   The local launch script takes care of everything and is the recommended way
   to spin things up. It will tear down, rebuild and start the
   containers as well

   Simply run:

   ```bash
   ./bin/launch.sh
   ```

2. ### Using Docker Compose

   Using docker compose to spin up the application.
   It'll setup a postgres database, redis, app workers, a celery beat instance,
   and flower for monitoring.

   Simply run:

   ```bash
   docker-compose --env-file ./config/common.env up
   ```

   This spins up several things and ties everything together:
   - Database
   - Redis
   - 2 Worker clients
   - Celery beat
   - Flower

   _NOTE: The `WORKER_REPLICA_COUNT` environment variable controls the number
   of worker instances to be spawned._

3. ### Pythonic way

   Sometimes it takes time to spin up the containers. So you can use the more
   pythonic ways to get the application running. The following things have to
   be made available first:

   - [Redis](./project-setup.md#running-redis)
   - [PostgreSQL](./project-setup.md#running-postgres)
   - [Install the dependencies](./project-setup.md#installation)
   - [Load environment variables](./project-setup.md#load-environment-variables)

   With that done, you can run different parts of the application independently.

   #### Initialize the database
   This will run the `init_db` task to create tables in Postgres and then
   populate the data from csv files present in `data/` directory.

   ```
   celery -A booktech call booktech.internal.tasks.init_db
   ```

   #### Spin up the worker
   The worker process will do the major task of executing each task

   ```
   celery -A booktech worker --loglevel=INFO
   ```

   #### Start the beat!
   To run the periodic task enable celery beat. This loads
   `booktech.internal.tasks.load_all` every 10 seconds.

   ```
   celery -A booktech beat --loglevel=INFO
   ```

   #### Watch it bloom!
   It's always nice to see monitoring. Flower makes a neat dashboard
   available at [http://localhost:5555](http://localhost:5555) by default.
   Head over to the webpage, to see available workers and all the tasks in
   different states.

   ```
   celery -A booktech flower --loglevel=INFO
   ```

### Load environment variables

In order to run the application, you need some environment variables in place.
All the variables are stored in `config` folder.

For development, use the ones in `config/common.env` file.

> Note:
>
> To load environment variables if you're a terminal person, you might want
> to use [direnv](https://direnv.net/). Simply, make the variables present
> in `config/*.env` file available by exporting them in a `.envrc` file
> at the root directory.

## Running Redis

1. If you have a Redis locally
   [installed](https://redis.io/docs/getting-started/installation/) then it's
   fairly easy to run it. Simply run:
   ```
   redis-server
   ```
   This will make the server available at `localhost:6379`

2. _(Recommended)_ The other way is to run Redis via docker compose. Simply run:
   ```
   docker compose up redis
   ```
   This will make the server available at `localhost:6379` using default port forwarding.


## Running PostgreSQL

1. _(Recommended)_ The best way is to run PostgreSQL via docker compose. Simply run:
   ```
   docker compose up db
   ```
   This will make the database available at `localhost:5432` using default port forwarding.

2. Via docker run
   ```
   docker run --env-file=.env -p $DB_HOST_PORT:$DB_REMOTE_PORT -v $DB_MOUNT_VOLUME:$PGDATA postgres:latest
   ```

3. If you have a PostgreSQL locally
   [installed](https://www.postgresql.org/download/) then it's fairly easy to
   run it. Run the following to check if it's already running:
   ```
   systemctl status postgresql
   ```
   or any other command based on your OS.

   This will make the server available at `localhost:5432` by default.


### Connect to postgres via psql

The password is available as an environment variable `PGPASSWORD` in the `common.env`
file. The `psql` command will automatically authenticate using that else it'll prompt for a password
```
psql -h 127.0.0.1 -p $DB_HOST_PORT -d $POSTGRES_DB -U $POSTGRES_USER
```

