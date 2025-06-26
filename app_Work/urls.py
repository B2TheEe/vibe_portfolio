from django.urls import path
from . import views

urlpatterns = [
    path('', views.work_experience, name='work_experience'),
]
