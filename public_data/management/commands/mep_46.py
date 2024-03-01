import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand


logger = logging.getLogger("management.commands")


class Command(BaseCommand):
    help = "Data migration for version 4.6"

    def handle(self, *args, **options) -> None:
        logger.info("Start mep_46")

        call_command("maintenance", on=True)

        logger.info("Update SCoT SIREN")
        call_command("update_scot_siren", all=True)

        logger.info("Migrate to admin_express referential")
        call_command("initial_loading", clean=True)

        call_command("maintenance", off=True)
        logger.info("End mep_46")
