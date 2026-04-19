from django.contrib import admin
from .models import GitHubProject

@admin.register(GitHubProject)
class GitHubProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('skills',)