# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run development server
python manage.py runserver

# Apply migrations
python manage.py migrate

# Create and apply new migrations after model changes
python manage.py makemigrations
python manage.py migrate

# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test app_Skills

# Collect static files
python manage.py collectstatic

# Create a superuser for admin access
python manage.py createsuperuser
```

## Architecture

This is a Django 4.2 portfolio website for Bente Schopman, structured as a multi-app project with bilingual support (English/Dutch).

### App structure

Each section of the portfolio is a separate Django app:

| App | URL prefix | Purpose |
|-----|-----------|---------|
| `app_AboutMe` | `/` (root) | Homepage with bio, photo, and CV download |
| `app_Education` | `/education` | Education history |
| `app_Work` | `/work/` | Work experience |
| `app_Skills` | `/skills/` | Skills grouped by category with rating |
| `app_Blog` | `/blog/` | Blog posts with CKEditor rich text |
| `app_Portfolio` | `/portfolio/` | GitHub projects showcase |

### Bilingual content pattern

All models store bilingual content with explicit `_nl` and `_en` field suffixes (e.g., `title_nl`, `title_en`). Views manually select the correct field based on `translation.get_language()` or `request.LANGUAGE_CODE`. There is **no** `modeltranslation` translation registration file — language switching is done manually in views.

Language switching uses Django's built-in `i18n_patterns` and the `set_language` view via a navbar dropdown. The `LocaleMiddleware` is the first middleware entry so URL prefixes like `/en/` and `/nl/` are active.

### Templates

All templates extend `templates/app_All/base.html`, which includes Bootstrap 5 (via CDN), Bootstrap Icons, and a custom `static/css/styles.css`. Template directories follow the `templates/<app_name>/` convention.

### Rich text / media

- `app_Blog` uses `django-ckeditor` (`RichTextUploadingField`) for blog post content. Uploads go to `media/uploads/`.
- Other apps use `ImageField`/`FileField` with various `upload_to` subdirectories under `media/`.
- `MEDIA_URL` and `MEDIA_ROOT` are configured and served in development via `urlpatterns += static(...)`.

### Database

SQLite (`db.sqlite3`) used for development. No production database configuration is present.

### Static files

Custom static files live in `static/`. The `staticfiles/` directory contains collected output from `collectstatic` and should not be edited directly.
