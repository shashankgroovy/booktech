# BookTech

Its a simple API that compares prices.

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
