# Generated by Django 4.2.5 on 2023-09-07 17:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("public_data", "0097_remove_scot_date_acting_remove_scot_date_end_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scot",
            name="siren",
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name="Siren"),
        ),
    ]