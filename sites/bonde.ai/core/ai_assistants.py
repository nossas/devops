# from django.utils import timezone
from django.db import transaction
from django_ai_assistant import AIAssistant, method_tool

from apps.website_tools.models import Site, Domain, HttpRouter


class BondeAIAssistant(AIAssistant):
    id = "bonde_assistant"
    name = "Bonde Assistant"
    instructions = (
        "You are a robot responsible for helping users use our website administration tools."
        "You are not allowed to add a domain to a site that is not found, when this happens you must notify the user that the Site does not exist and cannot be created."
        "When asked to create a campaign you should suggest the user to create a website and add a domain and an http router."
    )
    model = "gpt-4o"

    # def get_instructions(self):
    #     return f"{self.instructions} Today is {timezone.now().isoformat()}."

    def raise_user_not_found(self):
        if not self._user:
            raise Exception("You need to authenticate with a user")
    
    @method_tool
    def fetch_websites(self, name: str = None) -> dict:
        """Fetch list websites of User and use name to filter this list."""
        self.raise_user_not_found()

        qs = Site.objects.for_user(self._user).all()

        if name:
            qs = qs.filter(name__icontains=name)

        return {
            "websites": list(qs.values("id", "name", "community__name"))
        }

    @method_tool
    def create_domain(self, domain_name: str, site_id: int, purchase_at=None, expired_at=None) -> str:
        """Create a domain to website. Must has pass name and site id"""
        self.raise_user_not_found()

        try:
            site = Site.objects.for_user(self._user).get(id=site_id)

            with transaction.atomic():
                Domain.objects.update_or_create(
                    name=domain_name,
                    defaults={
                        "site": site,
                        "purchase_at": purchase_at,
                        "expired_at": expired_at
                    }
                )
            
            return f"Added {domain_name} domain to {site.name}." 
        except Site.DoesNotExist:
            return f"Website {site_id} not found."
        except Exception:
            return "We had a problem trying to create the domain."
    
    @method_tool
    def fetch_domains(self, name: str = None) -> dict:
        """Fetch list domains of User and use name to filter this list."""
        self.raise_user_not_found()

        qs = Domain.objects.for_user(self._user).all()

        if name:
            qs = qs.filter(name__icontains=name)

        return {
            "domains": list(qs.values("id", "name", "purchase_at", "expired_at", "site__id"))
        }

    @method_tool
    def create_http_router(self, domain_id: int, service_name: str) -> str:
        """Create a HttpRouter to domain. Must has pass domain id and service name"""
        self.raise_user_not_found()
        
        try:
            domain = Domain.objects.for_user(self._user).get(id=domain_id)

            with transaction.atomic():
                obj, _ = HttpRouter.objects.update_or_create(
                    name=domain.name.replace(".", "-"),
                    defaults={
                        "service": service_name
                    }
                )
                obj.domains.set([domain, ])
                obj.save()

        except Domain.DoesNotExist:
            return f"Domain {domain.name} not found."
        except Exception:
            return "We had a problem trying to create the http router."