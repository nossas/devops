# Generated by Django 5.1.2 on 2024-10-23 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website_tools", "0003_remove_domain_http_router_httprouter_domains"),
    ]

    operations = [
        migrations.AddField(
            model_name="httprouter",
            name="service",
            field=models.CharField(
                blank=True,
                choices="[('', ''), ('$bonde@docker', 'bonde'), ('$cms@docker', 'cms'), ('$traefik@docker', 'traefik'), ('$app@docker', 'app'), ('$localstack@docker', 'localstack'), ('$etcd@docker', 'etcd'), ('$whoami@docker', 'whoami'), ('$etcd-webui@docker', 'etcd-webui'), ('$pensive_kepler@docker', 'pensive_kepler'), ('$pensive_robinson@docker', 'pensive_robinson'), ('$serene_jang@docker', 'serene_jang'), ('$gallant_newton@docker', 'gallant_newton'), ('$elated_cartwright@docker', 'elated_cartwright'), ('$heuristic_jemison@docker', 'heuristic_jemison'), ('$epic_mirzakhani@docker', 'epic_mirzakhani'), ('$360forlabel-db-1@docker', '360forlabel-db-1'), ('$360forlabel-caddy-1@docker', '360forlabel-caddy-1'), ('$360forlabel-minio-1@docker', '360forlabel-minio-1'), ('$360forlabel-mailhog-1@docker', '360forlabel-mailhog-1'), ('$dev-minio-1@docker', 'dev-minio-1'), ('$cms-minio-1@docker', 'cms-minio-1'), ('$splitshare-postgres-1@docker', 'splitshare-postgres-1'), ('$dev-traefik-1@docker', 'dev-traefik-1'), ('$dev-redis-1@docker', 'dev-redis-1'), ('$dev-api-graphql-1@docker', 'dev-api-graphql-1')]",
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="httprouter",
            name="schema_history",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
