from app.config import settings
from celery import Celery
from app.tasks import email 


celery_app = Celery("app", broker=settings.REDIS_BROKER_URL, backend=settings.CELERY_BACKEND_URL)

celery_app.conf.update(
    task_routes={
        'task_default_queue': "default",
        'app.tasks.*': {'queue': 'default'},
    },
)

