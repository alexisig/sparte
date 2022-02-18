# Generated by Django 3.2.11 on 2022-02-11 23:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project", "0025_auto_20220120_1235"),
    ]

    operations = [
        migrations.CreateModel(
            name="Request",
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
                ("first_name", models.CharField(max_length=150, verbose_name="Prénom")),
                ("last_name", models.CharField(max_length=150, verbose_name="Nom")),
                (
                    "function",
                    models.CharField(
                        max_length=250, null=True, verbose_name="Fonction"
                    ),
                ),
                (
                    "organism",
                    models.CharField(
                        choices=[
                            ("AGENCE", "Agence d'urbanisme"),
                            ("AMENAG", "Aménageur"),
                            ("ASSOCI", "Association"),
                            ("BUREAU", "Bureau d'études"),
                            ("COMMUN", "Commune"),
                            ("DDT", "DDT"),
                            ("DEPART", "Département"),
                            ("DREAL", "DREAL"),
                            ("EPCI", "EPCI"),
                            ("EPF", "EPF"),
                            ("GIP", "GIP"),
                            ("PARTIC", "Particulier"),
                            ("REGION", "Région"),
                            ("SCOT", "SCOT"),
                            ("AUTRE", "Autre"),
                        ],
                        default="COMMUN",
                        max_length=30,
                        verbose_name="Organisme",
                    ),
                ),
                ("email", models.EmailField(max_length=254, verbose_name="E-mail")),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                (
                    "sent_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="date d'envoi"
                    ),
                ),
                (
                    "done",
                    models.BooleanField(default=False, verbose_name="A été envoyé ?"),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.project",
                        verbose_name="Projet",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="demandeur",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_date"],
            },
        ),
    ]