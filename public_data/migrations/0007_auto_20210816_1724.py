# Generated by Django 3.2.5 on 2021-08-16 17:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("public_data", "0006_auto_20210816_1723"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sybarval",
            name="a_b_2015_2",
            field=models.IntegerField(null=True, verbose_name="a_b_2015_2"),
        ),
        migrations.AlterField(
            model_name="sybarval",
            name="a_b_2018_2",
            field=models.IntegerField(null=True, verbose_name="a_b_2018_2"),
        ),
        migrations.AlterField(
            model_name="sybarval",
            name="a_brute_20",
            field=models.IntegerField(null=True, verbose_name="a_brute_20"),
        ),
        migrations.AlterField(
            model_name="sybarval",
            name="d_batie_20",
            field=models.FloatField(null=True, verbose_name="d_batie_20"),
        ),
        migrations.AlterField(
            model_name="sybarval",
            name="d_brute_20",
            field=models.FloatField(null=True, verbose_name="d_brute_20"),
        ),
        migrations.AlterField(
            model_name="sybarval",
            name="d_voirie_2",
            field=models.FloatField(null=True, verbose_name="d_voirie_2"),
        ),
        migrations.AlterField(
            model_name="sybarval",
            name="tache_2018",
            field=models.IntegerField(null=True, verbose_name="tache_2018"),
        ),
        migrations.AlterField(
            model_name="sybarval",
            name="voirie_201",
            field=models.IntegerField(null=True, verbose_name="voirie_201"),
        ),
        migrations.AlterField(
            model_name="sybarval",
            name="z_baties_2",
            field=models.IntegerField(null=True, verbose_name="z_baties_2"),
        ),
    ]
