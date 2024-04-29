import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand

from public_data.models import DataSource, Departement

logger = logging.getLogger("management.commands")


class Command(BaseCommand):
    help = "Dedicated to load data for 5.0 deployment"

    def load_departement(self, departement: Departement):
        call_command(
            command_name="load_shapefile",
            dataset=DataSource.DatasetChoices.OCSGE,
            land_id=departement.source_id,
        )
        call_command(
            command_name="build_commune_data",
            departement=departement.source_id,
            verbose=True,
        )
        call_command(
            command_name="import_gpu",
            departement=departement.source_id,
        )
        call_command(
            command_name="update_project_ocsge",
            departements=[departement.source_id],
        )

    def handle(self, *args, **options):
        logger.info("Start mep_5")

        call_command("maintenance", on=True)

        logger.info("Initialize data sources")
        # Since we are editing the data sources for Gers, we need to delete them first,
        # otherwise we will have duplicates for that departement
        deleted, _ = DataSource.objects.all().delete()
        logger.info(f"Deleted {deleted} data sources")
        call_command("loaddata", "public_data/models/data_source_fixture.json")

        logger.info("Load new OCS GE")
        call_command("setup_departements")

        departements_source_ids = [
            "69",  # Rhône
            "38",  # Isère
            "37",  # Indre-et-Loire
            "29",  # Finistère
            "11",  # Aude
            "67",  # Bas-Rhin
            "84",  # Vaucluse
            "32",  # Gers
        ]

        for source_id in departements_source_ids:
            departement = Departement.objects.get(source_id=source_id)
            self.load_departement(departement)

        call_command("maintenance", off=True)
        logger.info("End mep_5")