# Generated by Django 4.2.5 on 2023-09-07 17:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("public_data", "0096_cerema_aav2020txt_cerema_art09fer22_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="scot",
            name="date_acting",
        ),
        migrations.RemoveField(
            model_name="scot",
            name="date_end",
        ),
        migrations.RemoveField(
            model_name="scot",
            name="date_published_perimeter",
        ),
        migrations.RemoveField(
            model_name="scot",
            name="date_stop",
        ),
        migrations.RemoveField(
            model_name="scot",
            name="date_validation",
        ),
        migrations.RemoveField(
            model_name="scot",
            name="departement",
        ),
        migrations.RemoveField(
            model_name="scot",
            name="detailed_state_statut",
        ),
        migrations.RemoveField(
            model_name="scot",
            name="is_ene_law",
        ),
        migrations.RemoveField(
            model_name="scot",
            name="is_inter_departement",
        ),
        migrations.RemoveField(
            model_name="scot",
            name="region",
        ),
        migrations.RemoveField(
            model_name="scot",
            name="scot_type",
        ),
        migrations.RemoveField(
            model_name="scot",
            name="state_statut",
        ),
        migrations.AddField(
            model_name="scot",
            name="departements",
            field=models.ManyToManyField(to="public_data.departement"),
        ),
        migrations.AddField(
            model_name="scot",
            name="regions",
            field=models.ManyToManyField(to="public_data.region"),
        ),
    ]