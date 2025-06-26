from django.db import models

class WorkExperience(models.Model):
    title_nl = models.CharField(max_length=200, verbose_name="Titel in Nederlands")
    title_en = models.CharField(max_length=200, verbose_name="Title in English")
    company_nl = models.CharField(max_length=200, verbose_name="Bedrijf in Nederlands")
    company_en = models.CharField(max_length=200, verbose_name="Company in English")
    description_nl = models.TextField(verbose_name="Beschrijving in Nederlands")
    description_en = models.TextField(verbose_name="Description in English")
    start_date = models.DateField(verbose_name="Startdatum")
    end_date = models.DateField(verbose_name="Einddatum", null=True, blank=True)
    is_current = models.BooleanField(default=False, verbose_name="Huidige baan")
    logo = models.ImageField(upload_to='logos/', verbose_name="Logo", null=True, blank=True)

    def __str__(self):
        return self.title_en
