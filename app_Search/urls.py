from django.urls import path
from . import views

app_name = 'app_Search'

urlpatterns = [
    path('', views.search, name='search'),
]
