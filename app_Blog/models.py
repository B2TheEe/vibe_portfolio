from django.conf import settings
from django.db import models
from django.utils import translation
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    name_nl = models.CharField(max_length=100, verbose_name="Naam in Nederlands")
    name_en = models.CharField(max_length=100, verbose_name="Name in English")

    def __str__(self):
        return self.name_en


class BlogPost(models.Model):
    title_nl = models.CharField(max_length=200, verbose_name="Titel (NL)")
    title_en = models.CharField(
        max_length=200, verbose_name="Title (EN)", blank=True,
        help_text="Leeg = toon de Nederlandse titel ook op de Engelse site.",
    )
    content_nl = CKEditor5Field(config_name='default', verbose_name="Inhoud (NL)")
    content_en = CKEditor5Field(
        config_name='default', verbose_name="Content (EN)", blank=True,
        help_text="Leeg = toon de Nederlandse inhoud ook op de Engelse site.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    main_image = models.ImageField(upload_to='blog_main_images/', null=True, blank=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='posts'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='blog_posts',
        verbose_name='Author',
    )

    @property
    def display_title(self):
        if translation.get_language() == 'en':
            return self.title_en or self.title_nl
        return self.title_nl or self.title_en

    @property
    def display_content(self):
        if translation.get_language() == 'en':
            return self.content_en or self.content_nl
        return self.content_nl or self.content_en

    def __str__(self):
        return self.title_nl or self.title_en
