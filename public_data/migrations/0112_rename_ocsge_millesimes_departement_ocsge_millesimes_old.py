# Generated by Django 4.2.7 on 2023-12-11 16:18

import re
from django.db import migrations, models
import django.contrib.postgres.fields


def transfer_ocsge_millesimes(apps, schema_editor):
    Departement = apps.get_model("public_data", "Departement")
    for departement in Departement.objects.exclude(ocsge_millesimes_old__isnull=True):
        matches = re.finditer(r"([\d]{4,4})", departement.ocsge_millesimes_old)
        departement.ocsge_millesimes = [int(m.group(0)) for m in matches]
        departement.save()


def reverse_transfer_ocsge_millesimes(apps, schema_editor):
    Departement = apps.get_model("public_data", "Departement")
    for departement in Departement.objects.exclude(ocsge_millesimes__isnull=True):
        new_millesimes = " ".join(map(str, departement.ocsge_millesimes))
        departement.ocsge_millesimes_old = new_millesimes
        departement.save()


class Migration(migrations.Migration):
    dependencies = [
        ("public_data", "0111_remove_commune_ocsge_coverage_status_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="departement",
            old_name="ocsge_millesimes",
            new_name="ocsge_millesimes_old",
        ),
        migrations.AddField(
            model_name="departement",
            name="ocsge_millesimes",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(), blank=True, null=True, size=None
            ),
        ),
        migrations.RunPython(transfer_ocsge_millesimes, reverse_code=reverse_transfer_ocsge_millesimes),
        migrations.RemoveField(
            model_name="departement",
            name="ocsge_millesimes_old",
        ),
    ]