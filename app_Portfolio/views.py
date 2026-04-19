from django.shortcuts import render
from .models import GitHubProject

def github_projects(request):
    projects = GitHubProject.objects.prefetch_related('skills').all()
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

    return render(request, 'app_Portfolio/github_projects.html', {'projects': projects})

