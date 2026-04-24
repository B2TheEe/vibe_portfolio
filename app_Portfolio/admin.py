from django.contrib import admin
from .models import GitHubProject, PortfolioItem

@admin.register(GitHubProject)
class GitHubProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('skills',)

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    filter_horizontal = ('skills',)