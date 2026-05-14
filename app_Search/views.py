from django.shortcuts import render
from django.utils.translation import get_language
from django.db.models import Q

from app_Blog.models import BlogPost
from app_Portfolio.models import GitHubProject
from app_Skills.models import Skill

_MAX_QUERY_LEN = 100
_MIN_QUERY_LEN = 2
_RESULTS_PER_SECTION = 5


def _clean_query(raw):
    """Normalize whitespace and enforce max length.
    SQL injection is prevented by the ORM; XSS by Django's template auto-escaping."""
    return ' '.join(raw.strip()[:_MAX_QUERY_LEN].split())


def search(request):
    raw_query = request.GET.get('q', '')
    query = _clean_query(raw_query)
    lang = get_language() or 'en'

    blog_results = []
    portfolio_results = []
    skill_results = []
    too_short = bool(raw_query.strip() and len(query) < _MIN_QUERY_LEN)

    if query and len(query) >= _MIN_QUERY_LEN:
        blog_results = list(
            BlogPost.objects
            .filter(Q(title__icontains=query) | Q(content__icontains=query))
            .select_related('category')
            .order_by('-created_at')[:_RESULTS_PER_SECTION]
        )

        portfolio_results = list(
            GitHubProject.objects
            .filter(
                Q(title_nl__icontains=query) | Q(title_en__icontains=query) |
                Q(description_nl__icontains=query) | Q(description_en__icontains=query)
            )[:_RESULTS_PER_SECTION]
        )

        skill_results = list(
            Skill.objects
            .filter(
                Q(name_nl__icontains=query) | Q(name_en__icontains=query) |
                Q(description_nl__icontains=query) | Q(description_en__icontains=query)
            )
            .select_related('category')[:_RESULTS_PER_SECTION]
        )

    total = len(blog_results) + len(portfolio_results) + len(skill_results)

    return render(request, 'app_Search/search_results.html', {
        'query': query,
        'blog_results': blog_results,
        'portfolio_results': portfolio_results,
        'skill_results': skill_results,
        'total': total,
        'too_short': too_short,
        'lang': lang,
    })
