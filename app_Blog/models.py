from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
    name_nl = models.CharField(max_length=100, verbose_name="Naam in Nederlands")
    name_en = models.CharField(max_length=100, verbose_name="Name in English")

    def __str__(self):
        return self.name_en


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = CKEditor5Field(config_name='default')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    main_image = models.ImageField(upload_to='blog_main_images/', null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='posts')

    def __str__(self):
        return self.title

