from http.client import HTTPResponse
from .tasks import send_telegram_message
from django.http import HttpResponse
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
import json

# Create your views here.
def index(request):
    # Giving this task to celery
    send_telegram_message.delay()
    return HttpResponse("Congratulations! All sessages sent Successfully")

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