# Generated by Django 5.2.3 on 2025-06-24 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_AboutMe", "0002_remove_aboutme_cv_aboutme_cv_en_aboutme_cv_nl"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aboutme",
            name="cv_en",
            field=models.FileField(
                blank=True, null=True, upload_to="media/", verbose_name="CV in English"
            ),
        ),
        migrations.AlterField(
            model_name="aboutme",
            name="cv_nl",
            field=models.FileField(
                blank=True, null=True, upload_to="media/", verbose_name="CV in Dutch"
            ),
        ),
        migrations.AlterField(
            model_name="aboutme",
            name="photo",
            field=models.ImageField(upload_to="media/"),
        ),
    ]
