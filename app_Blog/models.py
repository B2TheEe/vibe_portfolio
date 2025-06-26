from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class BlogImage(models.Model):
    image = models.ImageField(upload_to='blog_images/')

class BlogPost(models.Model):
    title_nl = models.CharField(max_length=200, verbose_name="Titel in Nederlands")
    title_en = models.CharField(max_length=200, verbose_name="Title in English")
    content_nl = RichTextUploadingField(verbose_name="Inhoud in Nederlands")
    content_en = RichTextUploadingField(verbose_name="Content in English")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Aangemaakt op")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Bijgewerkt op")
    images = models.ManyToManyField(BlogImage, blank=True, verbose_name="Afbeeldingen")

    def __str__(self):
        return self.title_en
