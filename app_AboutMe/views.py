from django.shortcuts import render
from django.utils import translation
from .models import AboutMe

def about_me(request):
    about_me_info = AboutMe.objects.first()  # Assuming you have only one "About Me" entry

    # Detect the user's language
    user_language = translation.get_language()

    # Pass the appropriate content based on the user's language
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

    #return render(request, 'about_me.html', context)
    return render(request, 'app_AboutMe/about_me.html', context)

