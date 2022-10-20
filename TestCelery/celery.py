import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab # For celery-beat schedule at this time


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestCelery.settings')

# To set project as an application for celery to work with
app = Celery('TestCelery')

# Config for celery beat[To schedule the tasks once or in a time interval]
app.conf.beat_schedule = {
    
}
'''
Manually create a task to see dynamic go to view.py
app.conf.beat_schedule = {
    'send-telegram-messages':{
        'task':'MainApp.tasks.send_telegram_message',
        'schedule': crontab(hour=17, minute=18)
    }  
}
'''

# Disable defualt UTC timezone setting
app.conf.enable_utc = False

# Now to set Indian time zone
app.conf.update(timezone = "Asia/Kolkata")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')