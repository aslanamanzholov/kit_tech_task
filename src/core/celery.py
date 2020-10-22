from __future__ import (
    absolute_import, unicode_literals
)

import datetime
from datetime import datetime as dt
from os import environ

from celery import Celery
from django.utils.timezone import localtime

environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


class MyCelery(Celery):
    def now(self) -> dt:
        return localtime()


celery_app = MyCelery('core')
celery_app.config_from_object(
    obj='django.conf:settings', namespace='CELERY'
)
celery_app.autodiscover_tasks()

celery_app.conf.CELERY_BEAT_SCHEDULE = {
    'equipment': {
        'task': 'core.schedules.send_email_to_executor',
        'schedule': datetime.timedelta(days=1),
    },
}