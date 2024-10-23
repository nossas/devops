from django.contrib import admin

from .models import Site, Domain, HttpRouter


class DomainAdmin(admin.ModelAdmin):
    list_display = ("name", "hosted_zone_id", "purchase_at", "expired_at")
    fields = ("name", "purchase_at", "expired_at", "has_manage_dns", "site")
    autocomplete_fields = ("http_routers", )

admin.site.register(Domain, DomainAdmin)


class SiteAdmin(admin.ModelAdmin):
    list_display = ("name", "community", "created_at", "updated_at")

admin.site.register(Site, SiteAdmin)


class HttpRouterAdmin(admin.ModelAdmin):
    list_display = ("name", "priority", "service")
    fields = ("name", "service", "priority", "schema_history", "domains")
    search_fields = ("name", )
    readonly_fields = ("schema_history", )

admin.site.register(HttpRouter, HttpRouterAdmin)