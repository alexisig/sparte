# Generated by Django 3.2.5 on 2021-08-25 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("public_data", "0008_artifcommune"),
        ("project", "0005_auto_20210825_1559"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="cities",
            field=models.ManyToManyField(
                to="public_data.ArtifCommune", verbose_name="cities"
            ),
        ),
    ]