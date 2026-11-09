from django import forms
from django.core.exceptions import ValidationError
from django_ckeditor_5.widgets import CKEditor5Widget
from PIL import Image
from .models import BlogPost

_MAX_IMAGE_SIZE_MB = 5
_ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
_ALLOWED_PIL_FORMATS = {'JPEG', 'PNG', 'WEBP', 'GIF'}
_MAX_CONTENT_BYTES = 200 * 1024  # 200 KB


class BlogPostForm(forms.ModelForm):
    content_nl = forms.CharField(widget=CKEditor5Widget(config_name='default'), label="Inhoud (NL)")
    content_en = forms.CharField(
        widget=CKEditor5Widget(config_name='default'), required=False, label="Content (EN)",
        help_text="Leeg = toon de Nederlandse inhoud ook op de Engelse site.",
    )

    class Meta:
        model = BlogPost
        fields = ['title_nl', 'title_en', 'content_nl', 'content_en', 'category', 'main_image']

    def clean_title_nl(self):
        title = self.cleaned_data.get('title_nl', '').strip()
        if not title:
            raise ValidationError("Titel (NL) mag niet leeg zijn.")
        return title

    def _clean_content_field(self, field_name):
        content = self.cleaned_data.get(field_name, '')
        if len(content.encode('utf-8')) > _MAX_CONTENT_BYTES:
            raise ValidationError(
                "Inhoud is te groot (maximaal 200 KB)."
            )
        return content

    def clean_content_nl(self):
        content = self._clean_content_field('content_nl')
        if not content.strip():
            raise ValidationError("Inhoud (NL) mag niet leeg zijn.")
        return content

    def clean_content_en(self):
        return self._clean_content_field('content_en')

    def clean_main_image(self):
        image = self.cleaned_data.get('main_image')
        if not image or not hasattr(image, 'content_type'):
            return image

        if image.content_type not in _ALLOWED_IMAGE_TYPES:
            raise ValidationError(
                "Alleen JPEG-, PNG-, WEBP- en GIF-afbeeldingen zijn toegestaan."
            )
        if image.size > _MAX_IMAGE_SIZE_MB * 1024 * 1024:
            raise ValidationError(
                f"De afbeelding mag maximaal {_MAX_IMAGE_SIZE_MB} MB groot zijn."
            )

        # Verify actual file content via magic bytes — content_type is client-supplied
        # and trivially spoofable. Pillow reads the file header to determine format.
        try:
            image.seek(0)
            img = Image.open(image)
            if img.format not in _ALLOWED_PIL_FORMATS:
                raise ValidationError(
                    "Alleen JPEG-, PNG-, WEBP- en GIF-afbeeldingen zijn toegestaan."
                )
            img.verify()
        except ValidationError:
            raise
        except Exception:
            raise ValidationError("Ongeldig of beschadigd afbeeldingsbestand.")
        finally:
            image.seek(0)

        return image
