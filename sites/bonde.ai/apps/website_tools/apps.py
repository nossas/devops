from django.apps import AppConfig


class WebsiteToolsAppConfig(AppConfig):
    name = "apps.website_tools"

    def ready(self) -> None:
        from django.db.models.signals import pre_save, pre_delete, m2m_changed
        from apps.website_tools.models import Domain, HttpRouter
        from apps.website_tools.signals import (
            update_or_create_dns_hosted_zone,
            delete_dns_hosted_zone,
            update_or_create_traefik_http_router,
            delete_traefik_http_router
        )

        pre_save.connect(update_or_create_dns_hosted_zone, Domain)
        pre_delete.connect(delete_dns_hosted_zone, Domain)

        m2m_changed.connect(update_or_create_traefik_http_router, HttpRouter.domains.through)
        # post_save.connect(update_or_create_traefik_http_router, HttpRouter)
        pre_delete.connect(delete_traefik_http_router, HttpRouter)
