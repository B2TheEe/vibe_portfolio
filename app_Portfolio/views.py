from django.shortcuts import render
from .models import GitHubProject

def github_projects(request):
    projects = GitHubProject.objects.all()
    user_language = request.LANGUAGE_CODE

    for project in projects:
        if user_language == 'nl':
            project.title = getattr(project, 'title_nl', project.title_en)
            project.description = getattr(project, 'description_nl', project.description_en)
        else:
            project.title = project.title_en
            project.description = project.description_en

    return render(request, 'app_Portfolio/github_projects.html', {'projects': projects})

