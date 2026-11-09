from django.contrib import admin
from .models import BlogPost, Category

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title_nl', 'title_en', 'category', 'created_at')
    list_filter = ('category',)

admin.site.register(Category)
