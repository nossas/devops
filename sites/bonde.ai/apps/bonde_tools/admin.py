from django.contrib import admin

from .models import Community


class CommunityAdmin(admin.ModelAdmin):
    list_display = ("name", "external_id")


admin.site.register(Community, CommunityAdmin)