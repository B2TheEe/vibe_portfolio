from django.db import models

class GitHubProject(models.Model):
    title_nl = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    description_nl= models.TextField()
    description_en = models.TextField()
    github_url = models.URLField()
    image = models.ImageField(upload_to='projects/')

    def __str__(self):
        return self.title_nl