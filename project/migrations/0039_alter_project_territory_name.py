# Generated by Django 3.2.14 on 2022-07-29 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0038_project_territory_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="territory_name",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="Territoire"
            ),
        ),
    ]
