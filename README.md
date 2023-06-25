# BookTech

It's a simple application that compares prices b/w goods.
It also showcases the use of celery for scheduling task and offloading heavy work.

## Technical docs:

- [Installation and running the application](./docs/project-setup.md)
- [Directory Structure](./docs/directory-structure.md)
- [Errors](./docs/errors.md)
- [Problem Statement](./docs/problem.md)
- [Generated app output](./docs/app_output.md)
- [Monitoring](./docs/monitoring.md)

## Quickstart

The entire app is dockerized which makes it fairly easy to work with. Use the
following script to spin up the application.

```bash
bash bin/launch.sh
```

For more, read the [project setup guide](./docs/project-setup.md).

## Benchmarks
Based on a complete run, 50000 live price records were processed in under 8 mins and 16 seconds.
Therefore the application has a high throughput of processing 100 requests/second.

Monitoring support has been added to track the number of tasks being processed
and monitor the celery workload with the help of celery flower. Go to
[http://localhost:5555/](http://localhost:5555/)

Addtionally, we can use the same data from flower to power our Prometheus+Grafana dashboard
For more head over to [monitoring doc](./docs/monitoring.md) on how to set it up.

Here's a quick screenshot of the dashboard.
![Grafana Dashboard](./docs/Grafana-Celery-Monitoring-Dashboard.png)

## Style Guide

Follow the [Python style guide - PEP 8](https://www.python.org/dev/peps/pep-0008/)
and use [Black](https://pypi.org/project/black/) as the code formatter.

## Contributing

Just hack away and happy programming!
