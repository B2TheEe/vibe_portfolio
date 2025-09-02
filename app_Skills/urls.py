from django.urls import path
from . import views


app_name = "app_Skills"

urlpatterns = [
    path('', views.skills, name='skills'),
]
