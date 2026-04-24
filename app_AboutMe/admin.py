from django.contrib import admin
from django.contrib import messages
from .models import AboutMe

@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not AboutMe.objects.exists()

    def changelist_view(self, request, extra_context=None):
        obj = AboutMe.objects.first()
        if obj:
            from django.http import HttpResponseRedirect
            from django.urls import reverse
            return HttpResponseRedirect(
                reverse("admin:app_AboutMe_aboutme_change", args=[obj.pk])
            )
        return super().changelist_view(request, extra_context)
