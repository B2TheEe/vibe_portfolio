from django.shortcuts import render
from .models import GitHubProject
from app_Skills.models import Skill

LANGUAGE_KEYWORDS = {'taal', 'talen', 'language', 'languages'}

def _is_language_category(name):
    return any(kw in name.lower() for kw in LANGUAGE_KEYWORDS)

def github_projects(request):
    projects = GitHubProject.objects.prefetch_related('skills__category').all()
    user_language = request.LANGUAGE_CODE

    for project in projects:
        if user_language == 'nl':
            project.title = getattr(project, 'title_nl', project.title_en)
            project.description = getattr(project, 'description_nl', project.description_en)
            project.skill_names = [s.name_nl for s in project.skills.all()]
        else:
            project.title = project.title_en
            project.description = project.description_en
            project.skill_names = [s.name_en for s in project.skills.all()]
        project.skill_ids = ','.join(str(s.id) for s in project.skills.all())

    used_skills = (
        Skill.objects
        .filter(projects__isnull=False)
        .distinct()
        .select_related('category')
        .order_by('category__position', 'name_en')
    )

    language_skills = []
    other_skills = []
    for skill in used_skills:
        cat_nl = skill.category.name_nl
        cat_en = skill.category.name_en
        entry = {
            'id': skill.id,
            'name': skill.name_nl if user_language == 'nl' else skill.name_en,
        }
        if _is_language_category(cat_nl) or _is_language_category(cat_en):
            language_skills.append(entry)
        else:
            other_skills.append(entry)

    return render(request, 'app_Portfolio/github_projects.html', {
        'projects': projects,
        'language_skills': language_skills,
        'other_skills': other_skills,
    })

