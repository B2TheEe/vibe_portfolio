from django.shortcuts import render
from django.utils import translation
from .models import Category

def skills(request):
    categories = Category.objects.all().prefetch_related('skills')

    user_language = translation.get_language()

    context = {
        'categories': [{
            'name': category.name_en if user_language == 'en' else category.name_nl,
            'skills': [{
                'name': skill.name_en if user_language == 'en' else skill.name_nl,
                'description': skill.description_en if user_language == 'en' else skill.description_nl,
                'level': skill.level,
                'icon': skill.icon.url
            } for skill in category.skills.all()]
        } for category in categories]
    }

#return render(request, 'app_Skills/skills.html', context)

    return render(request, 'app_Skills/skills.html', context)

