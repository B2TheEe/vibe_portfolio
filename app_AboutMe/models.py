from django.db import models

class AboutMe(models.Model):
    title_nl = models.CharField(max_length=100, verbose_name="Title in Dutch")
    title_en = models.CharField(max_length=100, verbose_name="Title in English")
    description_nl = models.TextField(verbose_name="Description in Dutch")
    description_en = models.TextField(verbose_name="Description in English")
    bio_nl = models.TextField(verbose_name="Bio in Dutch")
    bio_en = models.TextField(verbose_name="Bio in English")
    photo = models.ImageField(upload_to='photos/')
    cv_nl = models.FileField(upload_to='cv/', verbose_name="CV in Dutch",  null=True, blank=True)
    cv_en = models.FileField(upload_to='cv/', verbose_name="CV in English", null=True, blank=True)

    def __str__(self):
        return self.title_en
