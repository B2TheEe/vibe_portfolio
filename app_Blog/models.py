from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Category(models.Model):
    name_nl = models.CharField(max_length=100, verbose_name="Naam in Nederlands")
    name_en = models.CharField(max_length=100, verbose_name="Name in English")

    def __str__(self):
        return self.name_en


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    main_image = models.ImageField(upload_to='blog_main_images/', null=True, blank=True)

    def __str__(self):
        return self.title

