from django.db import models
from django.core.exceptions import ValidationError

class GitHubProject(models.Model):
    title_nl = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    description_nl= models.TextField()
    description_en = models.TextField()
    github_url = models.URLField()
    image = models.ImageField(upload_to='projects/')
    skills = models.ManyToManyField('app_Skills.Skill', blank=True, related_name='projects', verbose_name="Skills")

    def __str__(self):
        return self.title_nl

    class Meta:
        abstract = False


class PortfolioItem(GitHubProject):
    url = models.URLField(verbose_name="Website URL")

    def clean(self):
        super().clean()
        if self.url and "github.com" in self.url.lower():
            raise ValidationError({"url": "Gebruik het veld 'GitHub URL' voor GitHub-links, niet dit veld."})

    def __str__(self):
        return self.title_nl

    class Meta:
        verbose_name = "Portfolio Item"
        verbose_name_plural = "Portfolio Items"