from django.contrib import admin
from .models import BlogPost , Category
from ckeditor.widgets import CKEditorWidget
from django import forms

class BlogPostAdminForm(forms.ModelForm):
    content_nl = forms.CharField(widget=CKEditorWidget())
    content_en = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = BlogPost
        fields = '__all__'

class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Category)
