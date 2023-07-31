# Generated by Django 4.2.3 on 2023-07-31 13:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trajectory", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trajectory",
            name="end",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(2021),
                    django.core.validators.MaxValueValidator(2075),
                ],
                verbose_name="Année de fin",
            ),
        ),
        migrations.AlterField(
            model_name="trajectory",
            name="start",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(2021),
                    django.core.validators.MaxValueValidator(2075),
                ],
                verbose_name="Année de début",
            ),
        ),
    ]