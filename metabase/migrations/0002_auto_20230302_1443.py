# Generated by Django 3.2.18 on 2023-03-02 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metabase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlinediagnostic',
            name='date_first_download',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date du premier téléchargement'),
        ),
        migrations.AddField(
            model_name='onlinediagnostic',
            name='is_downaloaded',
            field=models.BooleanField(default=False, verbose_name='A été téléchargé'),
        ),
    ]