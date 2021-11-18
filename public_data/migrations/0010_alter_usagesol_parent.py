# Generated by Django 3.2.5 on 2021-09-14 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("public_data", "0009_couverturesol_usagesol"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usagesol",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="public_data.usagesol",
            ),
        ),
    ]