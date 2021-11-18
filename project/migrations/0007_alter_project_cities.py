# Generated by Django 3.2.5 on 2021-08-27 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("public_data", "0008_artifcommune"),
        ("project", "0006_alter_project_cities"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="cities",
            field=models.ManyToManyField(
                blank=True, to="public_data.ArtifCommune", verbose_name="cities"
            ),
        ),
    ]