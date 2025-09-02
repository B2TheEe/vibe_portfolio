from django.urls import path
from . import views

app_name = "app_Work"

urlpatterns = [
    path('', views.work_experience, name='work_experience'),
]
