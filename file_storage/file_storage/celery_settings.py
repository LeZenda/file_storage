import os
import celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_storage.settings')

app = celery.Celery('file_storage')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
