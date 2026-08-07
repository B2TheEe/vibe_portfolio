from django.urls import path
from . import views

app_name = 'app_AboutMe'
urlpatterns = [
    path('', views.index, name='index'),
    path('cv/download/', views.download_cv, name='download_cv'),
]
