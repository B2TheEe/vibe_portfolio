from django.contrib import admin
from .models import BlogPost, BlogImage
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

class BlogPostAdminForm(forms.ModelForm):
    content_nl = forms.CharField(widget=CKEditorUploadingWidget())
    content_en = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = BlogPost
        fields = '__all__'

class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogImage)
