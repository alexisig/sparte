import logging

from django.core.management.base import BaseCommand
from django.db import connection

from admin_express import models as new
from public_data.models import administration as old


logger = logging.getLogger("management.commands")


class Command(BaseCommand):
    help = "Initialize admin_express ref using old public_data.models.administration ref."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clean",
            action="store_true",
            help="Clean all data before loading",
        )

    def handle(self, *args, **options) -> None:
        logger.info("Start initializing admin_express ref")

        # remove previous loaded data if required
        if options.get("clean"):
            self.truncate_all_tables()

        # initialize all layers
        self.create_regions()
        self.create_departements()
        self.create_scots()
        self.create_epcis()
        self.create_communes()

        # add linked information
        self.create_dept_links()
        self.create_scot_links()
        self.create_epci_links()
        self.create_commune_links()

        logger.info("End initializing admin_express ref")

    def truncate_all_tables(self) -> None:
        logger.info("Truncating tables of new referential")
        with connection.cursor() as cursor:
            for model in [new.AdminTerritory, new.Region, new.Departement, new.Epci, new.Commune, new.Scot]:
                cursor.execute(f'TRUNCATE TABLE "{model._meta.db_table}" RESTART IDENTITY CASCADE')

    def create_regions(self) -> None:
        to_create = old.Region.objects.exclude(source_id__in=new.Region.objects.values_list("official_id", flat=True))
        logger.info("Creating missing regions: %d items", to_create.count())
        for old_region in to_create:
            new.Region.objects.create(
                category=new.AdminTerritory.CATEGORY.REGION,
                official_id=old_region.source_id,
                name=old_region.name,
                mpoly=old_region.mpoly,
            )

    def create_departements(self) -> None:
        to_create = old.Departement.objects.exclude(
            source_id__in=new.Departement.objects.values_list("official_id", flat=True)
        )
        logger.info("Creating missing departements: %d items", to_create.count())
        for old_dept in to_create:
            new.Departement.objects.create(
                category=new.AdminTerritory.CATEGORY.DEPARTEMENT,
                official_id=old_dept.source_id,
                name=old_dept.name,
                mpoly=old_dept.mpoly,
                is_artif_ready=old_dept.is_artif_ready,
                ocsge_millesimes=old_dept.ocsge_millesimes,
                srid_source=old_dept.srid_source,
            )

    def create_scots(self) -> None:
        processed_siren = new.Scot.objects.exclude(official_id__startswith="Unknown").values_list(
            "official_id", flat=True
        )
        processed_id = [
            int(_.replace("Unknown-", ""))
            for _ in new.Scot.objects.filter(official_id__startswith="Unknown").values_list("official_id", flat=True)
        ]
        to_create = old.Scot.objects.all().exclude(siren__in=processed_siren).exclude(id__in=processed_id)

        logger.info("Creating missing SCoTs: %d items", to_create.count())

        for old_scot in to_create:
            new.Scot.objects.create(
                category=new.AdminTerritory.CATEGORY.SCOT,
                official_id=old_scot.siren or f"Unknown-{old_scot.id}",  # id required for uniquness
                name=old_scot.name,
                mpoly=old_scot.mpoly,
                srid_source=old_scot.srid_source,
            )

    def create_epcis(self) -> None:
        to_create = old.Epci.objects.exclude(source_id__in=new.Epci.objects.values_list("official_id", flat=True))
        logger.info("Creating missing EPCIs: %d items", to_create.count())
        for old_epci in to_create:
            new.Epci.objects.create(
                category=new.AdminTerritory.CATEGORY.EPCI,
                official_id=old_epci.source_id,
                name=old_epci.name,
                mpoly=old_epci.mpoly,
                srid_source=old_epci.srid_source,
            )

    def create_communes(self) -> None:
        to_create = old.Commune.objects.exclude(insee__in=new.Commune.objects.values_list("official_id", flat=True))
        logger.info("Creating missing communes: %d items", to_create.count())
        for old_comm in to_create:
            new.Commune.objects.create(
                category=new.AdminTerritory.CATEGORY.COMMUNE,
                official_id=old_comm.insee,
                name=old_comm.name,
                mpoly=old_comm.mpoly,
                srid_source=old_comm.srid_source,
                first_millesime=old_comm.first_millesime,
                last_millesime=old_comm.last_millesime,
                ocsge_available=old_comm.ocsge_available,
            )

    def create_dept_links(self) -> None:
        """Départements are linked to 1 region."""
        logger.info("Creating départements links")
        for old_dept in old.Departement.objects.all():
            new_dept = new.Departement.objects.get(official_id=old_dept.source_id)
            new_region = new.Region.objects.get(official_id=old_dept.region.source_id)
            new_dept.parents.add(new_region)

    def create_scot_links(self) -> None:
        logger.info("Creating SCoT links")
        for old_scot in old.Scot.objects.all():
            new_scot = new.Scot.objects.get(official_id__in=[old_scot.siren, f"Unknown-{old_scot.id}"])
            for old_dept in old_scot.departements.all():
                new_dept = new.Departement.objects.get(official_id=old_dept.source_id)
                new_scot.parents.add(new_dept)
                new_scot.parents.add(new_dept.get_region())

    def create_epci_links(self) -> None:
        """EPCI is linked to several departements."""
        logger.info("Creating EPCI links")
        for old_epci in old.Epci.objects.all():
            new_epci = new.Epci.objects.get(official_id=old_epci.source_id)
            for old_dept in old_epci.departements.all():
                new_dept = new.Departement.objects.get(official_id=old_dept.source_id)
                new_epci.parents.add(new_dept)
                new_epci.parents.add(new_dept.get_region())

    def create_commune_links(self) -> None:
        """Communes are linked to 1 EPCI, 1 SCoT and 1 Departement."""
        logger.info("Creating communes links")
        for old_comm in old.Commune.objects.all():
            new_comm = new.Commune.objects.get(official_id=old_comm.insee)
            # link departement
            new_dept = new.Departement.objects.get(official_id=old_comm.departement.source_id)
            new_comm.parents.add(new_dept)
            # link departement's region
            new_comm.parents.add(new_dept.get_region())
            # link epci
            if old_comm.epci:
                new_epci = new.Epci.objects.get(official_id=old_comm.epci.source_id)
                new_comm.parents.add(new_epci)
            # link scot
            if old_comm.scot:
                new_scot = new.Scot.objects.get(official_id__in=[old_comm.scot.siren, f"Unknown-{old_comm.scot.id}"])
                new_comm.parents.add(new_scot)
