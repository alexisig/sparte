# Generated by Django 4.2.13 on 2024-06-14 11:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("public_data", "0172_remove_zoneartificielle_public_data_millesi_5fb7c5_idx_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="zoneartificielle",
            name="departement",
            field=models.CharField(db_index=True, max_length=15, verbose_name="Département"),
        ),
    ]
