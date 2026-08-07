import cloudinary.utils
from django.shortcuts import render, redirect
from django.http import Http404
from django.utils import translation
from .models import AboutMe


def index(request):
    about_me_info = AboutMe.objects.first()
    user_language = translation.get_language()

    if user_language == 'nl':
        context = {
            'title': about_me_info.title_nl,
            'description': about_me_info.description_nl,
            'bio': about_me_info.bio_nl,
            'photo': about_me_info.photo,
            'cv': about_me_info.cv_nl,
        }
    else:
        context = {
            'title': about_me_info.title_en,
            'description': about_me_info.description_en,
            'bio': about_me_info.bio_en,
            'photo': about_me_info.photo,
            'cv': about_me_info.cv_en,
        }

    return render(request, 'app_AboutMe/about_me.html', context)


def download_cv(request):
    about_me_info = AboutMe.objects.first()
    user_language = translation.get_language()
    cv_field = about_me_info.cv_nl if user_language == 'nl' else about_me_info.cv_en

    if not cv_field or not cv_field.name:
        raise Http404

    url = cloudinary.utils.private_download_url(
        cv_field.name,
        'pdf',
        resource_type='raw',
        type='upload',
    )
    return redirect(url)

