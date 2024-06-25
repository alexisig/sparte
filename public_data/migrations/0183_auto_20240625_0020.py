# Generated by Django 4.2.13 on 2024-06-24 22:20

from django.db import migrations


def add_impermeable_to_ocsge_and_ocsge_diff(apps, schema_editor):
    Ocsge = apps.get_model("public_data", "Ocsge")
    OcsgeDiff = apps.get_model("public_data", "OcsgeDiff")

    impermeable_couvertures = [
        "CS1.1.1.1",  # Zones bâties
        "CS1.1.1.2",  # Zones non bâties
    ]

    Ocsge.objects.filter(
        is_impermeable=None,
        couverture__in=impermeable_couvertures,
    ).update(is_impermeable=True)

    Ocsge.objects.filter(
        is_impermeable=None,
    ).update(is_impermeable=False)

    OcsgeDiff.objects.filter(
        is_new_impermeable=None,
        cs_new__in=impermeable_couvertures,
    ).exclude(
        cs_old__in=impermeable_couvertures,
    ).update(is_new_impermeable=True)

    OcsgeDiff.objects.filter(
        is_new_not_impermeable=None,
        cs_old__in=impermeable_couvertures,
    ).exclude(
        cs_new__in=impermeable_couvertures,
    ).update(is_new_not_impermeable=True)

    OcsgeDiff.objects.filter(
        is_new_impermeable=None,
    ).update(is_new_impermeable=False)

    OcsgeDiff.objects.filter(
        is_new_not_impermeable=None,
    ).update(is_new_not_impermeable=False)


def reverse_add_impermeable_to_ocsge_and_ocsge_diff(apps, schema_editor):
    Ocsge = apps.get_model("public_data", "Ocsge")
    OcsgeDiff = apps.get_model("public_data", "OcsgeDiff")

    Ocsge.objects.update(is_impermeable=None)
    OcsgeDiff.objects.update(is_new_impermeable=None)
    OcsgeDiff.objects.update(is_new_not_impermeable=None)


class Migration(migrations.Migration):
    dependencies = [
        ("public_data", "0182_ocsge_is_impermeable_ocsgediff_is_new_impermeable_and_more"),
    ]

    operations = [
        migrations.RunPython(
            code=add_impermeable_to_ocsge_and_ocsge_diff,
            reverse_code=reverse_add_impermeable_to_ocsge_and_ocsge_diff,
        )
    ]
