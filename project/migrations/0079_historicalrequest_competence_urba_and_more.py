# Generated by Django 4.2.13 on 2024-06-03 16:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0078_merge_20240508_1022"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalrequest",
            name="competence_urba",
            field=models.BooleanField(default=False, verbose_name="Le territoire a-t-il la compétence urbanisme"),
        ),
        migrations.AddField(
            model_name="historicalrequest",
            name="du_en_cours",
            field=models.BooleanField(
                default=False, verbose_name="Le document d'urbanisme du territoire est-il en cours de revision"
            ),
        ),
        migrations.AddField(
            model_name="request",
            name="competence_urba",
            field=models.BooleanField(default=False, verbose_name="Le territoire a-t-il la compétence urbanisme"),
        ),
        migrations.AddField(
            model_name="request",
            name="du_en_cours",
            field=models.BooleanField(
                default=False, verbose_name="Le document d'urbanisme du territoire est-il en cours de revision"
            ),
        ),
    ]
