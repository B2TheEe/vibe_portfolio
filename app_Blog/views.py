from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import BlogPost
from .forms import BlogPostForm
from django.shortcuts import render
from django.utils import translation
from django.conf import settings
from .models import BlogPost

from django.conf import settings

from django.utils import translation

def blog_post_list(request):

    # Haal de blogposts op en render de template
    posts = BlogPost.objects.all()
    return render(request, 'app_Blog/blogpost_list.html', {'posts': posts})


def blog_post_detail(request, pk):
    # Stel de taalvoorkeur van de gebruiker in
    user_language = request.session.get(translation.LANGUAGE_SESSION_KEY, 'en')
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language

    # Haal de blogpost op en render de template
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'app_Blog/blogpost_detail.html', {'post': post})


def blog_post_new(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('app_Blog:blog_post_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'app_Blog/blogpost_edit.html', {'form': form})

def blog_post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('app_Blog:blog_post_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'app_Blog/blogpost_edit.html', {'form': form})
