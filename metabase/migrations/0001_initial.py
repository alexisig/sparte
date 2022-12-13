# Generated by Django 3.2.18 on 2023-03-02 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0050_auto_20230224_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineDiagnostic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(verbose_name='Date de création')),
                ('is_anonymouse', models.BooleanField(default=True, verbose_name='Est anonyme')),
                ('is_public', models.BooleanField(default=True, verbose_name='Est public')),
                ('administrative_level', models.CharField(blank=True, max_length=255, null=True, verbose_name='Niveau administratif')),
                ('analysis_level', models.CharField(max_length=255, verbose_name="Maille d'analyse")),
                ('start_date', models.DateField(verbose_name='Date de début')),
                ('end_date', models.DateField(verbose_name='Date de fin')),
                ('link', models.CharField(max_length=255, verbose_name='Lien vers le diagnostic')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='Commune')),
                ('epci', models.CharField(blank=True, max_length=255, null=True, verbose_name='EPCI')),
                ('scot', models.CharField(blank=True, max_length=255, null=True, verbose_name='SCoT')),
                ('departement', models.CharField(blank=True, max_length=255, null=True, verbose_name='Département')),
                ('region', models.CharField(blank=True, max_length=255, null=True, verbose_name='Région')),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.project', verbose_name="Diagnostic d'origine")),
            ],
        ),
    ]