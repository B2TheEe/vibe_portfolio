from django.shortcuts import render
from django.utils import translation
from .models import Education

def education(request):
    educations = Education.objects.all().order_by('-start_date')

    user_language = translation.get_language()

    context = {
        'educations': [{
            'title': education.title_en if user_language == 'en' else education.title_nl,
            'institution': education.institution_en if user_language == 'en' else education.institution_nl,
            'description': education.description_en if user_language == 'en' else education.description_nl,
            'start_date': education.start_date,
            'end_date': education.end_date,
            'propedeuse_date': education.propedeuse_date,
            'diploma_date': education.diploma_date,
            'is_current': education.is_current ,
            'logo': education.logo,
        } for education in educations]
    }

    return render(request, 'app_Education/education.html', context)
