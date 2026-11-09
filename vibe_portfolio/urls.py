"""
URL configuration for vibe_portfolio project.
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from two_factor.admin import AdminSiteOTPRequired
from two_factor.urls import urlpatterns as tf_urls

# Vereist OTP-verificatie (Google Authenticator) voor elke admin-pagina.
# Zonder bevestigd TOTP-device mag een ingelogde staff-gebruiker alleen bij
# de device-registratiepagina's (otp_totp/otp_static) om er één aan te maken.
admin.site.__class__ = AdminSiteOTPRequired

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include(tf_urls)),
]

urlpatterns += i18n_patterns(
    path('', include('app_AboutMe.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('blog/', include('app_Blog.urls')),
    path('skills/', include('app_Skills.urls')),
    path("education", include('app_Education.urls')),
    path('work/', include('app_Work.urls')),
    path('portfolio/', include('app_Portfolio.urls')),
    path('search/', include('app_Search.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
