from django import forms
from django.core.exceptions import ValidationError
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import BlogPost

_MAX_IMAGE_SIZE_MB = 5
_ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}


class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name='default'))

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category', 'main_image']

    def clean_main_image(self):
        image = self.cleaned_data.get('main_image')
        if image and hasattr(image, 'content_type'):
            if image.content_type not in _ALLOWED_IMAGE_TYPES:
                raise ValidationError(
                    "Alleen JPEG-, PNG-, WEBP- en GIF-afbeeldingen zijn toegestaan."
                )
            if image.size > _MAX_IMAGE_SIZE_MB * 1024 * 1024:
                raise ValidationError(
                    f"De afbeelding mag maximaal {_MAX_IMAGE_SIZE_MB} MB groot zijn."
                )
        return image
