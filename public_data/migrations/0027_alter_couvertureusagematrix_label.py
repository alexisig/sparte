# Generated by Django 3.2.5 on 2021-11-02 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("public_data", "0026_auto_20211029_0913"),
    ]

    operations = [
        migrations.AlterField(
            model_name="couvertureusagematrix",
            name="label",
            field=models.CharField(
                choices=[
                    ("ARTIF", "Artificiel"),
                    ("CONSU", "Consommé"),
                    ("NAF", "NAF"),
                    ("ARTIF_NOT_CONSU", "Artificiel non consommé"),
                    ("NONE", "Non renseigné"),
                ],
                default="NONE",
                max_length=20,
                verbose_name="Libellé",
            ),
        ),
    ]