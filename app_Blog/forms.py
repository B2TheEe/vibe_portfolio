from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    short_content_nl = forms.CharField(widget=CKEditorWidget(), label="Korte inhoud in Nederlands")
    short_content_en = forms.CharField(widget=CKEditorWidget(), label="Short content in English")
    content_nl = forms.CharField(widget=CKEditorWidget(), label="Inhoud in Nederlands")
    content_en = forms.CharField(widget=CKEditorWidget(), label="Content in English")

    class Meta:
        model = BlogPost
        fields = [
            'title',
            'short_content_nl',
            'short_content_en',
            'content_nl',
            'content_en',
            'main_image'
        ]
