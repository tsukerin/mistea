from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mistea.settings')
celery_app = Celery('mistea')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

app = Celery('mistea', broker='pyamqp://guest@localhost//')

app.conf.beat_schedule = {
    'update-subscription-counter': {
        'task': 'tasks.update_subscription_counter',
        'schedule': crontab(minute=0, hour=0),
    },
}

app.conf.timezone = 'UTC'