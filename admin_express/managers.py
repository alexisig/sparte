from __future__ import annotations

from django.db.models import Q, Manager, QuerySet
from model_utils.managers import InheritanceQuerySet, InheritanceManagerMixin

from utils.db import IntersectMixin


class AdminTerritoryQuerySet(InheritanceQuerySet):
    """Inherit from InheritanceQuerySet to keep all functionnalities."""

    def get_communes(self) -> QuerySet["Commune"]:
        return (
            self.model.objects.filter(Q(children__in=self) | Q(parents__in=self))
            .filter(category=self.model.CATEGORY.COMMUNE)
            .select_subclasses()
        )


class AdminTerritoryManagerMixin:
    _queryset_class = AdminTerritoryQuerySet

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).select_subclasses()


class AdminTerritoryManager(AdminTerritoryManagerMixin, InheritanceManagerMixin, IntersectMixin, Manager):
    """Order of mixins  is important to ensure _queryset_class contains our custom queryset."""
    pass
