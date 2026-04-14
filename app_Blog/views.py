from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.utils import translation
from django.conf import settings
from .models import BlogPost, Category
from .forms import BlogPostForm

POSTS_PER_PAGE = 6

def blog_post_list(request):
    lang = request.LANGUAGE_CODE
    category_id = request.GET.get('category')
    posts = BlogPost.objects.all().order_by('-created_at')

    if category_id:
        posts = posts.filter(category_id=category_id)

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'app_Blog/blogpost_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'lang': lang,
    })


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
