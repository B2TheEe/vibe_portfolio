from django.urls import path
from . import views

app_name =  "app_Education"
urlpatterns = [
    path('', views.education, name='education'),
]
