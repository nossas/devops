# Generated by Django 5.1.2 on 2024-10-21 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_community_external_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="siteproject",
            name="community",
        ),
        migrations.RemoveField(
            model_name="domain",
            name="site",
        ),
        migrations.DeleteModel(
            name="Community",
        ),
        migrations.DeleteModel(
            name="Domain",
        ),
        migrations.DeleteModel(
            name="SiteProject",
        ),
    ]
