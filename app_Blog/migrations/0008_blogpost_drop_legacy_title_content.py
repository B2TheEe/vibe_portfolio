from django.db import migrations, models
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app_Blog', '0007_copy_title_content_to_nl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='title',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='content',
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title_nl',
            field=models.CharField(max_length=200, verbose_name='Titel (NL)'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title_en',
            field=models.CharField(
                blank=True, max_length=200, verbose_name='Title (EN)',
                help_text='Leeg = toon de Nederlandse titel ook op de Engelse site.',
            ),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='content_nl',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Inhoud (NL)'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='content_en',
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True, verbose_name='Content (EN)',
                help_text='Leeg = toon de Nederlandse inhoud ook op de Engelse site.',
            ),
        ),
    ]
