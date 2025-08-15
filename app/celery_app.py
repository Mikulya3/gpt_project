from app.config import settings
from celery import Celery 


celery_app = Celery(
    "app",
    broker=settings.REDIS_BROKER_URL,
    backend=settings.CELERY_BACKEND_URL, 
    include=["app.tasks.email"],
)

celery_app.conf.update(
    task_default_queue="default",
)
celery_app.autodiscover_tasks(["app.tasks"])

import app.tasks.email 


