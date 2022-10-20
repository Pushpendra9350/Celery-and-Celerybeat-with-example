from django.urls import path
from MainApp import views
urlpatterns = [
    path("", views.index, name = "index"),
    path("Schedule-Task", views.schedule_task_dynamically, name = "schedule"),
    path("Interval-Task", views.schedule_interval_dynamically, name = "schedule")
]
