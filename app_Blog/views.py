from django.shortcuts import render
from django.utils import translation
from .models import BlogPost

def blog(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    user_language = translation.get_language()

    context = {
        'posts': [{
            'title': post.title_en if user_language == 'en' else post.title_nl,
            'content': post.content_en if user_language == 'en' else post.content_nl,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
            'images': post.images.all()
        } for post in posts]
    }

    return render(request, 'app_Blog/blogs.html', context)
