from django.db.models import Manager, QuerySet
from model_utils.managers import InheritanceQuerySet, InheritanceManagerMixin

from utils.db import IntersectMixin


class AdminTerritoryQuerySet(InheritanceQuerySet):
    """Inherit from InheritanceQuerySet to keep all functionnalities."""

    def get_communes(self) -> QuerySet["Commune"]:
        """Get all communes within territories of the queryset."""
        from admin_express.models import Commune

        # keep current selected commune
        current_communes = Commune.objects.filter(
            id__in=self.filter(category=Commune.CATEGORY.COMMUNE).values_list("id", flat=True)
        )
        # find all communes children of other selected territories
        commune_children = Commune.objects.filter(parents__in=self)
        # join both and remove duplicates
        return (current_communes | commune_children).distinct("id")


class AdminTerritoryManagerMixin:
    _queryset_class = AdminTerritoryQuerySet

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).select_subclasses()


class AdminTerritoryManager(AdminTerritoryManagerMixin, InheritanceManagerMixin, IntersectMixin, Manager):
    """Order of mixins  is important to ensure _queryset_class contains our custom queryset."""
