from celery import Celery

from datetime import timedelta
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'train_ecommerce.settings')

celery_app = Celery('train_ecommerce')

celery_app.autodiscover_tasks()

celery_app.conf.broker_url = 'amqp://localhost:5672'
celery_app.conf.result_backend = 'rpc://'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'pickle'
celery_app.conf.accept_content = ['json', 'pickle']
celery_app.conf.result_expired = timedelta(days=1)
celery_app.conf.task_always_eager = False
celery_app.conf.worker_prefetch_multiplier = 4


@celery_app.task
def mul(x, y):
    return x+y