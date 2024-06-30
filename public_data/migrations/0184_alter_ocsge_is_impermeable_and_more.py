# Generated by Django 4.2.13 on 2024-06-25 06:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("public_data", "0183_auto_20240625_0020"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ocsge",
            name="is_impermeable",
            field=models.BooleanField(verbose_name="Est imperméable"),
        ),
        migrations.AlterField(
            model_name="ocsgediff",
            name="is_new_impermeable",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="ocsgediff",
            name="is_new_not_impermeable",
            field=models.BooleanField(verbose_name="Aussi appelé désimperméabilisation"),
        ),
    ]