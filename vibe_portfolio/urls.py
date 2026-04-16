"""
URL configuration for vibe_portfolio project.
"""
import os

from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Admin-URL uit omgevingsvariabele — wijzig in .env voor productie
_admin_url = os.environ.get('DJANGO_ADMIN_URL', 'dashboard-beheer').strip('/') + '/'

urlpatterns = [
    path(_admin_url, admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', include('app_AboutMe.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('blog/', include('app_Blog.urls')),
    path('skills/', include('app_Skills.urls')),
    path("education", include('app_Education.urls')),
    path('work/', include('app_Work.urls')),
    path('portfolio/', include('app_Portfolio.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
