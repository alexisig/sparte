# Generated by Django 4.2.7 on 2024-06-17 15:59

from django.db import migrations, models

from users.models import User


def ventilate_user_organisms(apps, schema_editor):
    UserModel = apps.get_model("users", "User")

    mapping = {
        "AMENAG": "AUTRE",
        "EPF": "AUTRE",
        "GIP": "AUTRE",
        "DEPART": "DDT",
        "REGION": "DREAL",
    }

    for old, new in mapping.items():
        UserModel.objects.filter(organism=old).update(organism=new)

    for user in UserModel.objects.all():
        user.organism_group = User.get_group(user.organism)
        user.save()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0010_auto_20230302_1508"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="organism",
            field=models.CharField(
                choices=[
                    ("AGENCE", "Agence d'urbanisme"),
                    ("ASSOCI", "Association"),
                    ("BUREAU", "Bureau d'études"),
                    ("COMMUN", "Commune"),
                    ("DDT", "DDT"),
                    ("DDTM", "DDTM"),
                    ("DEAL", "DEAL"),
                    ("DREAL", "DREAL"),
                    ("DRIEAT", "DRIEAT"),
                    ("EPCI", "EPCI"),
                    ("PARTIC", "Particulier"),
                    ("SCOT", "SCOT"),
                    ("AUTRE", "Autre"),
                ],
                default="COMMUN",
                max_length=250,
                verbose_name="Organisme",
            ),
        ),
        migrations.RunPython(ventilate_user_organisms),
    ]
