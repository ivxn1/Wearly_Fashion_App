import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Wearly_Fashion_App.settings")
app = Celery("Wearly_Fashion_App")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
