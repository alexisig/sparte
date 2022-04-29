# Generated by Django 3.2.5 on 2021-09-23 23:43

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import public_data.models.mixins


class Migration(migrations.Migration):

    dependencies = [
        ("public_data", "0011_auto_20210920_1954"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ocsge2015",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "couverture",
                    models.CharField(
                        blank=True, max_length=254, verbose_name="Couverture du sol"
                    ),
                ),
                (
                    "usage",
                    models.CharField(
                        blank=True, max_length=254, verbose_name="Usage du sol"
                    ),
                ),
                ("millesime", models.DateField(verbose_name="Millésime")),
                (
                    "source",
                    models.CharField(blank=True, max_length=254, verbose_name="Source"),
                ),
                (
                    "origine",
                    models.CharField(
                        blank=True, max_length=254, verbose_name="Origine"
                    ),
                ),
                (
                    "origine2",
                    models.CharField(
                        blank=True, max_length=254, verbose_name="Origine1"
                    ),
                ),
                (
                    "ossature",
                    models.IntegerField(blank=True, null=True, verbose_name="Ossature"),
                ),
                (
                    "commentaire",
                    models.CharField(
                        blank=True, max_length=254, verbose_name="Commentaire"
                    ),
                ),
                (
                    "mpoly",
                    django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
                ),
            ],
            bases=(
                models.Model,
                public_data.models.mixins.AutoLoadMixin,
                public_data.models.mixins.DataColorationMixin,
            ),
        ),
    ]
