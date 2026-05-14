"""
Django settings for vibe_portfolio project.
"""
import os
from pathlib import Path

# Laad omgevingsvariabelen uit .env (alleen in ontwikkeling)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Beveiliging — alle gevoelige waarden uit omgevingsvariabelen
# ---------------------------------------------------------------------------

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError(
        "DJANGO_SECRET_KEY is niet ingesteld. "
        "Stel deze in als omgevingsvariabele of in het .env bestand."
    )

DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

_allowed = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost 127.0.0.1')
ALLOWED_HOSTS = [h.strip() for h in _allowed.replace(',', ' ').split() if h.strip()]


# ---------------------------------------------------------------------------
# Geïnstalleerde apps
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'cloudinary_storage',
    'cloudinary',
    'django_ckeditor_5',
    "app_AboutMe",
    'app_Skills',
    "app_Education",
    "app_Work",
    "app_Blog",
    'app_Portfolio',
    'app_Search',
    'bootstrap5',
]


# ---------------------------------------------------------------------------
# Middleware — SecurityMiddleware moet als eerste staan
# ---------------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",                  # EERSTE: HTTPS, headers
    "whitenoise.middleware.WhiteNoiseMiddleware",                     # Statische bestanden via Gunicorn
    "vibe_portfolio.middleware.PayloadSizeLimitMiddleware",           # Oversized payloads weigeren
    "vibe_portfolio.middleware.RateLimitMiddleware",                  # Rate limiting (na static files)
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware',            # Na sessions, vóór common
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "vibe_portfolio.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "vibe_portfolio.wsgi.application"


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

import dj_database_url

_database_url = os.environ.get('DATABASE_URL')
if _database_url:
    DATABASES = {
        'default': dj_database_url.config(default=_database_url, conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ---------------------------------------------------------------------------
# Cache — gebruikt door rate-limiting middleware
# ---------------------------------------------------------------------------
# Standaard: LocMemCache (in-process). Bij meerdere Gunicorn workers kan elke
# worker een eigen teller bijhouden. Gebruik voor productie een gedeelde cache
# (bijv. Redis) via de CACHE_URL omgevingsvariabele en django-redis.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}


# ---------------------------------------------------------------------------
# Upload-limieten — beschermt tegen oversized of misvormd POST-verkeer
# ---------------------------------------------------------------------------
# Maximale grootte van POST-velddata exclusief bestandsuploads (default 2.5 MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024   # 2 MB
# Grens waarboven bestanden naar schijf worden geschreven in plaats van geheugen
FILE_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024   # 2 MB
# Maximaal aantal POST-velden — voorkomt hash-flooding-aanvallen
DATA_UPLOAD_MAX_NUMBER_FIELDS = 50


# ---------------------------------------------------------------------------
# Wachtwoordvalidatie — minimaal 12 tekens
# ---------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ---------------------------------------------------------------------------
# Internationalisatie
# ---------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ('en', 'English'),
    ('nl', 'Dutch'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------------
# Statische en media bestanden
# ---------------------------------------------------------------------------

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ---------------------------------------------------------------------------
# Beveiligingsheaders — altijd actief
# ---------------------------------------------------------------------------

# Voorkomt dat browsers inhoud buiten frames laden (clickjacking)
X_FRAME_OPTIONS = 'DENY'

# Voorkomt MIME-type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# Beperkt Referer-informatie naar eigen domein
SECURE_REFERRER_POLICY = 'same-origin'

# Cookies alleen leesbaar via HTTP (niet via JavaScript)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# ---------------------------------------------------------------------------
# Beveiligingsheaders — activeer in productie via omgevingsvariabelen
# ---------------------------------------------------------------------------

# Stuur alle HTTP-verzoeken door naar HTTPS
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False') == 'True'

# Cookies alleen over HTTPS versturen
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'False') == 'True'

# HTTP Strict Transport Security
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


# ---------------------------------------------------------------------------
# Logging — beveiligingsgebeurtenissen worden vastgelegd
# ---------------------------------------------------------------------------

_log_dir = os.path.join(BASE_DIR, 'logs')
os.makedirs(_log_dir, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(_log_dir, 'security.log'),
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(_log_dir, 'errors.log'),
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['error_file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}


# ---------------------------------------------------------------------------
# CKEditor 5 — imageUpload verwijderd uit toolbar (beveiligingsrisico)
# ---------------------------------------------------------------------------

CKEDITOR_5_UPLOAD_PATH = 'uploads/'
CKEDITOR_5_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|',
            'bold', 'italic', 'underline', 'strikethrough', '|',
            'link', 'blockQuote', 'code', 'codeBlock', '|',
            'bulletedList', 'numberedList', '|',
            'insertTable', '|',
            'undo', 'redo',
        ],
        'height': '300px',
    },
}
