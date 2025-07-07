from django.urls import path
from . import views

app_name = 'app_Blog'

urlpatterns = [
    # URL voor het weergeven van een lijst van blogposts
    path('', views.blog_post_list, name='blog_post_list'),

    # URL voor het maken van een nieuwe blogpost
    path('new/', views.blog_post_new, name='blog_post_new'),

    # URL voor het bewerken van een bestaande blogpost
    path('<int:pk>/edit/', views.blog_post_edit, name='blog_post_edit'),

    # URL voor het weergeven van een enkele blogpost
    path('<int:pk>/', views.blog_post_detail, name='blog_post_detail'),
]
