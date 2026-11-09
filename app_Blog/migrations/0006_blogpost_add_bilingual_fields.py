from django.db import migrations, models
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app_Blog', '0005_blogpost_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='title_nl',
            field=models.CharField(default='', blank=True, max_length=200, verbose_name='Titel (NL)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='title_en',
            field=models.CharField(
                default='', blank=True, max_length=200, verbose_name='Title (EN)',
                help_text='Leeg = toon de Nederlandse titel ook op de Engelse site.',
            ),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='content_nl',
            field=django_ckeditor_5.fields.CKEditor5Field(default='', blank=True, verbose_name='Inhoud (NL)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='content_en',
            field=django_ckeditor_5.fields.CKEditor5Field(
                default='', blank=True, verbose_name='Content (EN)',
                help_text='Leeg = toon de Nederlandse inhoud ook op de Engelse site.',
            ),
        ),
    ]
