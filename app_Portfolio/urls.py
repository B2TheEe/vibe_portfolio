from django.urls import path
from . import views

app_name =  "app_Portfolio"
urlpatterns = [
         path('portfolio', views.github_projects, name='portfolio'),
    ]
