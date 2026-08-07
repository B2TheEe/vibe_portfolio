from django.db import models
from django.core.exceptions import ValidationError
from cloudinary_storage.storage import RawMediaCloudinaryStorage

class AboutMe(models.Model):
    title_nl = models.CharField(max_length=100, verbose_name="Title in Dutch")
    title_en = models.CharField(max_length=100, verbose_name="Title in English")
    description_nl = models.TextField(verbose_name="Description in Dutch")
    description_en = models.TextField(verbose_name="Description in English")
    bio_nl = models.TextField(verbose_name="Bio in Dutch")
    bio_en = models.TextField(verbose_name="Bio in English")
    photo = models.ImageField(upload_to='media/')
    cv_nl = models.FileField(upload_to='cv/', verbose_name="CV in Dutch", null=True, blank=True, storage=RawMediaCloudinaryStorage())
    cv_en = models.FileField(upload_to='cv/', verbose_name="CV in English", null=True, blank=True, storage=RawMediaCloudinaryStorage())

    def clean(self):
        if not self.pk and AboutMe.objects.exists():
            raise ValidationError("Er kan maar één About Me-item bestaan.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_en

    class Meta:
        verbose_name = "About Me"
        verbose_name_plural = "About Me"
