from django.db import models
from django.utils.functional import lazy

from apps.bonde_tools.models import Community
from apps.bonde_tools.managers import BondeToolsManager

from .docker_client import get_docker_services_choices


class Site(models.Model):
    name = models.CharField(max_length=26, unique=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BondeToolsManager("community__users")


class Domain(models.Model):
    name = models.CharField(max_length=26, unique=True)
    purchase_at = models.DateField(null=True, blank=True)
    expired_at = models.DateField(null=True, blank=True)
    has_manage_dns = models.BooleanField(default=True)
    hosted_zone_id = models.CharField(max_length=140, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="domains")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BondeToolsManager("site__community__users")

    def __str__(self):
        return self.name


class HttpRouter(models.Model):
    """TODO: Make to async on Etcd"""

    name = models.SlugField(max_length=30, unique=True)
    priority = models.IntegerField(null=True, blank=True)
    domains = models.ManyToManyField(Domain, related_name="http_routers")
    service = models.CharField(
        choices=lazy(get_docker_services_choices, tuple)(),
        max_length=50,
        blank=True,
        null=True,
    )
    schema_history = models.JSONField(default=dict, blank=True)

    objects = BondeToolsManager("domains__site__community__users")

    @property
    def prefix(self):
        return f"traefik/http/routers/{self.name}"

    def get_m2m_rule(self, pk_set):
        return self._get_rule(domains=Domain.objects.filter(pk__in=pk_set))

    def get_rule(self):
        return self._get_rule(domains=self.domains.all())

    def _get_rule(self, domains=[]):
        """TODO: Conferir se domínios estão ativos para então remover a regra"""
        key = self.prefix + "/rule"
        names = []
        extensions = []

        # Separa as extensões dos nomes de endereço
        for domain in domains:
            extensions.append(".".join(domain.name.split(".")[1:]))
            names.append(domain.name.split(".")[0])

        # Remove duplicidades
        names = list(set(names))
        extensions = list(set(extensions))

        value = f"HostRegexp(`((www\.)?([a-z0-9-]+\.)?({'|'.join(names)})\.({'|'.join(extensions)}))$`)"
        return key, value

    def get_service(self):
        key = self.prefix + "/service"
        return key, self.service

    def get_entrypoints(self):
        key = self.prefix + "/entrypoints"
        return key, "websecure"

    def get_tls(self):
        key = self.prefix + "/tls"
        return key, "true"

    def get_certresolver(self):
        key = self.prefix + "/tls/certresolver"
        return key, "myresolver"

    # etcdctl put traefik/http/routers/rnc-org/rule "HostRegexp(\`((www\.)?([a-z0-9-]+\.)?rnc\.(org|org.br))$\`)"

    # etcdctl put traefik/http/routers/rnc-org/service "public@docker"

    # etcdctl put traefik/http/routers/rnc-org/entrypoints "websecure"

    # etcdctl put traefik/http/routers/rnc-org/tls "true"

    # etcdctl put traefik/http/routers/rnc-org/tls/certresolver "myresolver"
