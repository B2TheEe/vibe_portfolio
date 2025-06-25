from django.db import models

# Define rating choices
RATING_CHOICES = (
    (1, 'Poor'),
    (2, 'Average'),
    (3, 'Good'),
    (4, 'Very Good'),
    (5, 'Excellent'),
)

class Category(models.Model):
    name_nl = models.CharField(max_length=100, verbose_name="Naam in Nederlands")
    name_en = models.CharField(max_length=100, verbose_name="Name in English")
    position = models.IntegerField(verbose_name="Positie", unique=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name_en

class Skill(models.Model):
    name_nl = models.CharField(max_length=100, verbose_name="Naam in Nederlands")
    name_en = models.CharField(max_length=100, verbose_name="Name in English")
    description_nl = models.TextField(verbose_name="Beschrijving in Nederlands")
    description_en = models.TextField(verbose_name="Description in English")
    level = models.IntegerField(choices=RATING_CHOICES, default=3, verbose_name="Niveau")
    icon = models.ImageField(upload_to='icons/', verbose_name="Icoon")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='skills', verbose_name="Categorie")

    def __str__(self):
        return self.name_en
