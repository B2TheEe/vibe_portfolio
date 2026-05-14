import re
import bleach
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.html import mark_safe
from django.core.paginator import Paginator
from .models import BlogPost, Category
from .forms import BlogPostForm

POSTS_PER_PAGE = 6

_ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 's',
    'a', 'ul', 'ol', 'li',
    'blockquote', 'code', 'pre',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
]

_DANGEROUS_SCHEME_RE = re.compile(
    r'^\s*(javascript|data|vbscript)\s*:', re.IGNORECASE
)


def _allow_safe_attrs(tag, name, value):
    """Allow only safe attributes; block dangerous URI schemes in href."""
    if tag == 'a':
        if name == 'href' and _DANGEROUS_SCHEME_RE.match(value):
            return False
        return name in ('href', 'title', 'rel')
    if tag in ('td', 'th'):
        return name in ('colspan', 'rowspan')
    return False


_ALLOWED_ATTRIBUTES = _allow_safe_attrs


def _sanitize_html(raw_html):
    cleaned = bleach.clean(
        raw_html,
        tags=_ALLOWED_TAGS,
        attributes=_ALLOWED_ATTRIBUTES,
        strip=True,
        strip_comments=True,
    )
    return mark_safe(cleaned)


def blog_post_list(request):
    lang = request.LANGUAGE_CODE
    posts = BlogPost.objects.all().order_by('-created_at')

    # Valideer category_id als integer om type-fouten te voorkomen
    category_id = None
    raw_category = request.GET.get('category', '').strip()
    if raw_category:
        try:
            category_id = int(raw_category)
            posts = posts.filter(category_id=category_id)
        except ValueError:
            pass  # Ongeldige waarde genegeerd

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
    post = get_object_or_404(BlogPost, pk=pk)
    sanitized_content = _sanitize_html(post.content)
    return render(request, 'app_Blog/blogpost_detail.html', {
        'post': post,
        'content': sanitized_content,
    })


@login_required
def blog_post_new(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('app_Blog:blog_post_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'app_Blog/blogpost_edit.html', {'form': form})


@login_required
def blog_post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        raise PermissionDenied
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('app_Blog:blog_post_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'app_Blog/blogpost_edit.html', {'form': form})
