# Generated by Django 4.2.13 on 2024-06-26 10:45

from django.db import migrations


def move_cover_image_from_project_to_landstaticfigure(apps, schema_editor):
    Project = apps.get_model("project", "Project")
    LandStaticFigure = apps.get_model("public_data", "LandStaticFigure")

    for project in (
        Project.objects.all()
        .filter(land_id__isnull=False)
        .only(
            "analyse_start_date",
            "analyse_end_date",
            "first_year_ocsge",
            "last_year_ocsge",
            "look_a_like",
            "name",
            "territory_name",
            "level",
            "target_2031",
            "cover_image",
            "land_type",
            "land_id",
        )
        .iterator()
    ):
        params = {
            "analyse_start_date": project.analyse_end_date,
            "analyse_end_date": project.analyse_end_date,
            "first_year_ocsge": project.last_year_ocsge,
            "last_year_ocsge": project.last_year_ocsge,
            "look_a_like": project.look_a_like,
            "name": project.name,
            "territory_name": project.territory_name,
            "level": project.level,
            "target_2031": project.target_2031,
        }
        params_hash = str(hash(frozenset(params.items())))
        if project.cover_image:
            LandStaticFigure.objects.create(
                land_type=project.land_type,
                land_id=project.land_id,
                figure=project.cover_image,
                figure_name="cover_image",
                params=params,
                params_hash=params_hash,
            )


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0083_alter_historicalrequest_organism_and_more"),
    ]

    operations = [
        migrations.RunPython(
            move_cover_image_from_project_to_landstaticfigure,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name="historicalproject",
            name="cover_image",
        ),
        migrations.RemoveField(
            model_name="project",
            name="cover_image",
        ),
    ]
