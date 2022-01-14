# Generated by Django 3.2.5 on 2022-01-14 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0022_auto_20220111_2211"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="public_key",
        ),
        migrations.AddField(
            model_name="project",
            name="look_a_like",
            field=models.CharField(
                help_text="We need a way to find Project related within Cerema's data. this is the purpose of this field which has a very specific rule of construction, it's like a slug: epci=EPCI_[ID], departement=DEPART_[ID], region=REGION_[ID]. field can contain several public key separate by ;",
                max_length=250,
                null=True,
                verbose_name="Territoire pour se comparer",
            ),
        ),
    ]