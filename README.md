### Basic setup of celery in a project
##### What is celery?
Celery is like a new worker to perform some of the tasks. So earlier Django was performing all the tasks but now django will give tasks to celery.
Question is why we need do that, because Django's main task is to server to the client and if django will perform any task then client needs to wait to compelete the task then client's experience will be bad. So we give time taking tasks to celery.
##### Installation
```git
pip install celery
```
##### Add these configurations to your settings.py file
```py
# Celery configurations 
CELERY_BROKER_URL = "redis://127.0.0.1:6379" 
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TIMEZONE = "Asia/Kolkata"
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

# Django celery results config
CELERY_RESULT_BACKEND = "django-db"

# Dajngo celery beat config
CELERY_BEAT_SCHEDULAR = "django_celery_beat.schedulers:DatabaseScheduler"
```
##### ProjectFolder/celery.py
```py
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestCelery.settings')

# To set project as an application for celery to work with
app = Celery('TestCelery')

# Config for celery beat[To schedule the tasks once or in a time interval]
app.conf.beat_schedule = {

}

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
```
Then
##### ProjectFolder/__inti__.py
```py
from .celery import app as celery_app

__all__ = ("celery_app",)
```
##### Create AppFolder/task.py
```py
from celery import shared_task

@shared_task
def test_task():
    for i in range(10):
        print(i)
    return "Done"
```
##### Inside AppFolder/views.py
```py
from http.client import HTTPResponse
from .tasks import test_task
from django.http import HttpResponse
# Create your views here.
def test(request):
    test_task.delay()
    return HttpResponse("Done from view")

def schedule_task_dynamically(request):
    schedule, created = CrontabSchedule.objects.get_or_create(minute = '6', hour = '18')
    task = PeriodicTask.objects.create(crontab = schedule,task = "MainApp.tasks.send_telegram_message", name = "schedule_message_3") #To send some argument to task function -> args = json.dumps([[2,3]]))
    return HttpResponse("Task Created Successfully")

def schedule_interval_dynamically(request):
    """
    IntervalSchedule.DAYS
    IntervalSchedule.HOURS
    IntervalSchedule.MINUTES
    IntervalSchedule.SECONDS
    IntervalSchedule.MICROSECONDS
    """
    schedule, created = IntervalSchedule.objects.get_or_create(every=60,period=IntervalSchedule.SECONDS)
    task = PeriodicTask.objects.create(interval = schedule,task = "MainApp.tasks.send_telegram_message", name = "schedule_message_4") #To send some argument to task function -> args = json.dumps([[2,3]]))
    return HttpResponse("Task Created Successfully")
```
##### To start celery workers
```git
celery -A TestCelery.celery worker -l INFO
```
##### Inorder to save the tasks results to Django DB
Insall
```git
pip install django-celery-results
```
And add this `CELERY_RESULT_BACKEND = "django-db"` to your settings.py
also add this `django_celery_results` to insatlled apps and migrate

##### Now to install Django celery beat
Celery beat is user to schedule a task or repeat a task in an interval
```git
pip install django-celery-beat
```
And add this `django_celery_beat` to your installed apps and `migrate`
also add this `CELERY_BEAT_SCHEDULAR = "django_celery_beat.schedulers:DatabaseScheduler"` to settings.py

Inside ProjectFolder/celery.py add
```py
app.conf.beat_schedule = {

}
```
##### To start celery beat
```git
celery -A TestCelery beat -l INFO
```
##### To start celery beat with database scheduler(In this db we have tasks so it will read and perform accordingly)
```git
celery -A TestCelery beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
Important Link: https://www.nickmccullum.com/celery-django-periodic-tasks/#periodic-tasks