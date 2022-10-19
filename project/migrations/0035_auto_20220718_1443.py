# Generated by Django 3.2.14 on 2022-07-18 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0034_auto_20220623_1344"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="analyse_end_date",
            field=models.CharField(
                choices=[
                    ("2009", "2009"),
                    ("2010", "2010"),
                    ("2011", "2011"),
                    ("2012", "2012"),
                    ("2013", "2013"),
                    ("2014", "2014"),
                    ("2015", "2015"),
                    ("2016", "2016"),
                    ("2017", "2017"),
                    ("2018", "2018"),
                    ("2019", "2019"),
                ],
                default="2018",
                max_length=4,
                verbose_name="Année de fin de période d'analyse",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="analyse_start_date",
            field=models.CharField(
                choices=[
                    ("2009", "2009"),
                    ("2010", "2010"),
                    ("2011", "2011"),
                    ("2012", "2012"),
                    ("2013", "2013"),
                    ("2014", "2014"),
                    ("2015", "2015"),
                    ("2016", "2016"),
                    ("2017", "2017"),
                    ("2018", "2018"),
                    ("2019", "2019"),
                ],
                default="2015",
                max_length=4,
                verbose_name="Année de début de période d'analyse",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="land_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("COMM", "Commune"),
                    ("EPCI", "EPCI"),
                    ("DEPART", "Département"),
                    ("REGION", "Région"),
                    ("COMP", "Composite"),
                ],
                default="EPCI",
                help_text="Indique le niveau administratif des territoires sélectionnés par l'utilisateur lors de la création du diagnostic. Cela va de la commune à la région.",
                max_length=7,
                null=True,
                verbose_name="Type de territoire",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="level",
            field=models.CharField(
                choices=[
                    ("COMM", "Commune"),
                    ("EPCI", "EPCI"),
                    ("DEPART", "Département"),
                    ("REGION", "Région"),
                    ("COMP", "Composite"),
                ],
                default="COMMUNE",
                help_text="Utilisé lors de la création des rapports afin de déterminer le niveau d'aggrégation des données à afficher. Si l'utilisateur a sélectionné EPCI, alors les rapports doivent montrer des données EPCI par EPCI.",
                max_length=7,
                verbose_name="Niveau d'analyse",
            ),
        ),
    ]