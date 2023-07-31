import logging

from django.core.management.base import BaseCommand

from metabase.models import StatDiagnostic
from trajectory.models import Trajectory

logger = logging.getLogger("management.commands")


class Command(BaseCommand):
    help = "Migrate trajectory if required"

    def handle(self, *args, **options):
        logger.info("migrate_trajectory_data")
        qs = Trajectory.objects.all()
        total = qs.count()
        logger.info(f"To process = {total}")
        for i, trajectory in enumerate(qs):
            trajectory.data = {y: {"value": v, "updated": False} for y, v in trajectory.data.items() if int(y) >= 2021}
            trajectory.save()
            stat = StatDiagnostic.get_or_create(trajectory.project)
            if stat.analysis_level is None:
                stat.update_with_project(trajectory.project)
            stat.update_with_trajectory(trajectory)
            if i % 100 == 0:
                print(f"{i + 1}/{total}")
        print(f"{i + 1}/{total}")
        logger.info("End migrate_trajectory_data")