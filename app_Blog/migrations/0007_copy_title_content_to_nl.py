from django.db import migrations


def copy_forwards(apps, schema_editor):
    BlogPost = apps.get_model('app_Blog', 'BlogPost')
    for post in BlogPost.objects.all():
        post.title_nl = post.title
        post.content_nl = post.content
        post.save(update_fields=['title_nl', 'content_nl'])


def copy_backwards(apps, schema_editor):
    BlogPost = apps.get_model('app_Blog', 'BlogPost')
    for post in BlogPost.objects.all():
        post.title = post.title_nl
        post.content = post.content_nl
        post.save(update_fields=['title', 'content'])


class Migration(migrations.Migration):

    dependencies = [
        ('app_Blog', '0006_blogpost_add_bilingual_fields'),
    ]

    operations = [
        migrations.RunPython(copy_forwards, copy_backwards),
    ]
