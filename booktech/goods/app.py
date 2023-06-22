from celery import Celery

from booktech.utils import configurator


cfg = configurator.load_yaml_config()
app = Celery('booktech',
             broker=cfg['celery']['broker_url'],
             backend=cfg['celery']['backend_url'])

# Configure Celery
app.conf.update(
    task_concurrency=cfg['celery']['task_concurrency'],
    worker_heartbeat=cfg['celery']['worker_heartbeat'],
    worker_prefetch_multiplier=cfg['celery']['worker_prefetch_multiplier'],
)

app.conf.beat_schedule = {
    'load-livedata-every-10-seconds': {
        'task': 'booktech.goods.tasks.load_all',
        'schedule': 10.0
    },
}
