# Generated by Django 4.2.7 on 2024-02-15 08:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0070_alter_historicalproject_land_id_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalproject",
            old_name="async_add_similar_lands_done",
            new_name="async_add_comparison_lands_done",
        ),
        migrations.RenameField(
            model_name="project",
            old_name="async_add_similar_lands_done",
            new_name="async_add_comparison_lands_done",
        ),
    ]
