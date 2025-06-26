from django.shortcuts import render
from django.utils import translation
from .models import WorkExperience

def work_experience(request):
    experiences = WorkExperience.objects.all().order_by('-start_date')

    user_language = translation.get_language()

    context = {
        'experiences': [{
            'title': experience.title_en if user_language == 'en' else experience.title_nl,
            'company': experience.company_en if user_language == 'en' else experience.company_nl,
            'description': experience.description_en if user_language == 'en' else experience.description_nl,
            'start_date': experience.start_date,
            'end_date': experience.end_date,
            'is_current': experience.is_current,
            'logo': experience.logo.url if experience.logo else None
        } for experience in experiences]
    }

    return render(request, 'app_Work/work_experience.html', context)
