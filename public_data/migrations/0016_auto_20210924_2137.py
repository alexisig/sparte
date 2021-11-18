# Generated by Django 3.2.5 on 2021-09-24 21:37

from django.db import migrations, models
from django.db.models import Value
from django.db.models.functions import Concat


def set_couverture(apps, schema_editor):
    CouvertureSol = apps.get_model("public_data", "CouvertureSol")
    CouvertureSol.objects.all().update(code_prefix=Concat(Value("CS"), "code"))


def set_usage(apps, schema_editor):
    UsageSol = apps.get_model("public_data", "UsageSol")
    UsageSol.objects.all().update(code_prefix=Concat(Value("US"), "code"))


class Migration(migrations.Migration):

    dependencies = [
        ("public_data", "0015_ocsge2015_map_color"),
    ]

    operations = [
        # process CouvertureSol
        migrations.AddField(
            model_name="couverturesol",
            name="code_prefix",
            field=models.CharField(
                max_length=10,
                null=True,
                blank=True,
                verbose_name="Nomenclature préfixée",
            ),
        ),
        migrations.RunPython(set_couverture, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="couverturesol",
            name="code_prefix",
            field=models.CharField(
                max_length=10, unique=True, verbose_name="Nomenclature préfixée"
            ),
        ),
        migrations.AddField(
            model_name="usagesol",
            name="code_prefix",
            field=models.CharField(
                max_length=10,
                null=True,
                blank=True,
                verbose_name="Nomenclature préfixée",
            ),
        ),
        migrations.RunPython(set_usage, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="usagesol",
            name="code_prefix",
            field=models.CharField(
                max_length=10, unique=True, verbose_name="Nomenclature préfixée"
            ),
        ),
    ]