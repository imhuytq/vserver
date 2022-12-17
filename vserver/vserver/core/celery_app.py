from celery import Celery

from vserver.config import config

BROKER_URL = "redis://{}:{}".format(config.REDIS_HOST, config.REDIS_PORT)
celery_app = Celery("worker", broker=BROKER_URL)

celery_app.conf.task_routes = {
    "vserver.worker.test_celery": "main-queue",
    "vserver.worker.get_video_info": "main-queue",
}
