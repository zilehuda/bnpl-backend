from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

# setting the Django settings module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "mark-installments-late-at-12am": {
        "task": "apps.bnpl.tasks.mark_installments_as_late",
        "schedule": crontab(hour=0, minute=0),  # at 12am
    },
    "remind-payment-at-12am": {
        "task": "apps.bnpl.tasks.remind_payment",
        "schedule": crontab(hour=0, minute=0),  # at 12am
    },
}
