from celery import Celery

BROKER_URL = "redis://127.0.0.1:6379/0"
celery_app = Celery("worker", broker=BROKER_URL)

celery_app.conf.task_routes = {
    "vserver.worker.test_celery": "main-queue",
    "vserver.worker.get_video_info": "main-queue",
}
