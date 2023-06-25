# Directory Structure

```
.
├── bin
├── booktech
│   ├── db
│   ├── internal
│   └── utils
├── config
├── data
└── docs
```

## Root level

At the root level, you'll find:

- Dockerfile, docker compose file for containerzing and running things locally.
- Requirements file for installing python packages.

## bin

The `bin` folder contains the `launch.sh` script for running the application
locally using docker compose.

## booktech

The `booktech` folder is where the entire application is packaged and can be
run as a celery project. It has 3 sub folders:

- **db** - Holds database configurations and initializer scripts.
- **internal** - Holds celery tasks, app model
- **utils** - Holds utility files like logger, cache and configuration loader.

## config

The `config` folder contains yaml file configurations to work with different environments.
Additionally, it also holds the environment variables required for running the application.

## data

The `data` folder is a placeholder location where csv files are kept.

## docs

The `docs` folder contains all the documentation.

