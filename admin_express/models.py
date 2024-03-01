from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Sum, Q, QuerySet

from admin_express.managers import AdminTerritoryManager
from public_data.models.enums import SRID
from public_data.models.cerema import Cerema


class AdminTerritory(models.Model):
    class CATEGORY(models.TextChoices):
        REGION = "REGION", "Région"
        DEPARTEMENT = "DEPART", "Département"
        EPCI = "EPCI", "EPCI"
        COMMUNE = "COMM", "Commune"
        SCOT = "SCOT", "SCoT"

    category = models.CharField("Catégorie", max_length=20, choices=CATEGORY.choices, db_index=True)
    official_id = models.CharField("Identifiant officiel", max_length=50, db_index=True)
    name = models.CharField("Nom", max_length=150, db_index=True)
    mpoly = models.MultiPolygonField(srid=4326)
    srid_source = models.IntegerField(
        "SRID",
        choices=SRID.choices,
        default=SRID.LAMBERT_93,
    )
    area = models.DecimalField("Surface", max_digits=15, decimal_places=4, blank=True, null=True)
    surface_artif = models.DecimalField(
        "Surface artificielle",
        max_digits=15,
        decimal_places=4,
        blank=True,
        null=True,
    )

    # In order to ease dev, should include all relations even if transitivity exist.
    # For instance, consider:
    # * commune A is in departement B
    # * departement B is in region C
    # then C should be listed as parent of A
    parents = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="children")

    class Meta:
        unique_together = (("category", "official_id"),)

    def public_key(self) -> str:
        return f"{self.category}_{self.official_id}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}:{self.public_key()}"

    def __str__(self) -> str:
        return f"{self.public_key()} - {self.name}"

    def __equal__(self, other: "AdminTerritory") -> bool:
        return self.public_key() == other.public_key()

    objects = AdminTerritoryManager()

    # from AdminRef
    @classmethod
    def get_default_analysis_level(cls, level: CATEGORY) -> CATEGORY:
        default_analysis = {
            cls.CATEGORY.COMMUNE: cls.CATEGORY.COMMUNE,
            cls.CATEGORY.EPCI: cls.CATEGORY.COMMUNE,
            cls.CATEGORY.SCOT: cls.CATEGORY.EPCI,
            cls.CATEGORY.DEPARTEMENT: cls.CATEGORY.SCOT,
            cls.CATEGORY.REGION: cls.CATEGORY.DEPARTEMENT,
        }
        try:
            return default_analysis[level]
        except KeyError:
            return cls.CATEGORY.COMMUNE

    @classmethod
    def get_available_analysis_level(cls, category: CATEGORY) -> list[CATEGORY]:
        available = {
            cls.CATEGORY.COMMUNE: [cls.CATEGORY.COMMUNE],
            cls.CATEGORY.EPCI: [cls.CATEGORY.COMMUNE],
            cls.CATEGORY.SCOT: [
                cls.CATEGORY.COMMUNE,
                cls.CATEGORY.EPCI,
            ],
            cls.CATEGORY.DEPARTEMENT: [
                cls.CATEGORY.COMMUNE,
                cls.CATEGORY.EPCI,
                cls.CATEGORY.SCOT,
            ],
            cls.CATEGORY.REGION: [
                cls.CATEGORY.COMMUNE,
                cls.CATEGORY.EPCI,
                cls.CATEGORY.SCOT,
                cls.CATEGORY.DEPARTEMENT,
            ],
        }
        try:
            return available[category]
        except KeyError:
            return [
                cls.CATEGORY.COMMUNE,
                cls.CATEGORY.EPCI,
                cls.CATEGORY.SCOT,
                cls.CATEGORY.DEPARTEMENT,
                cls.CATEGORY.REGION,
            ]

    # def default_analysis_level(self) -> CATEGORY:
    #     return self.get_default_analysis_level(self.category)

    def get_qs_cerema(self) -> QuerySet[Cerema]:
        raise NotImplementedError("Need to be specified in child")

    # Helpers to browse referential

    def helper_get_linked_territories(self, category: CATEGORY) -> QuerySet["AdminTerritory"]:
        """Select parents and children of current instance then filter them to get only the requested category."""
        return (
            AdminTerritory.objects.all()
            .filter(Q(children=self) | Q(parents=self))
            .filter(category=category)
            .distinct("id")
        )

    def get_regions(self) -> QuerySet["Region"]:
        """Return all linked regions."""
        return self.helper_get_linked_territories(AdminTerritory.CATEGORY.REGION)

    def get_departements(self) -> QuerySet["Departement"]:
        """Return all linked départements."""
        return self.helper_get_linked_territories(AdminTerritory.CATEGORY.DEPARTEMENT)

    def get_scots(self) -> QuerySet["Scot"]:
        """Return all linked SCoTs."""
        return self.helper_get_linked_territories(AdminTerritory.CATEGORY.SCOT)

    def get_epcis(self) -> QuerySet["Epci"]:
        """Return all linked EPCIs."""
        return self.helper_get_linked_territories(AdminTerritory.CATEGORY.EPCI)

    def get_communes(self) -> QuerySet["Commune"]:
        """Return all linked communes."""
        return self.helper_get_linked_territories(AdminTerritory.CATEGORY.COMMUNE)

    def get_region(self) -> "Region":
        """Helper to return the region linked to this instance.

        :exceptions: MultipleObjectsReturned if multiple regions are linked
        """
        return self.get_regions().get()

    def get_departement(self) -> "Departement":
        """Helper to return the departement linked to this instance.

        :exceptions: MultipleObjectsReturned if multiple departements are linked
        """
        return self.get_departements().get()

    def get_scot(self) -> "Scot":
        """Helper to return the SCoT linked to this instance.

        :exceptions: MultipleObjectsReturned if multiple SCoTs are linked
        """
        return self.get_scots().get()

    def get_epci(self) -> "Epci":
        """Helper to return the departement linked to this instance.

        :exceptions: MultipleObjectsReturned if multiple EPCIs are linked
        """
        return self.get_epcis().get()

    def get_commune(self) -> "Commune":
        """Helper to return the departement linked to this instance.

        :exceptions: MultipleObjectsReturned if multiple communes are linked
        """
        return self.get_communes().get()

    # Compatibility requirements, to be questionned

    def get_conso_per_year(self, start="2010", end="2020", coef=1):
        """Return Cerema data for the city, transposed and named after year"""
        fields = Cerema.get_art_field(start, end)
        qs = self.get_qs_cerema()
        args = (Sum(field) for field in fields)
        qs = qs.aggregate(*args)
        return {f"20{key[3:5]}": val * coef / 10000 for key, val in qs.items()}

    def get_ocsge_millesimes(self) -> set:
        """Return available OCS GE in linked departements."""
        millesimes = set()
        for dept in self.get_departements():
            millesimes.update(dept.ocsge_millesimes)
        return millesimes

    def is_artif_ready(self) -> bool:
        """Return True if all linked departements are also artif ready."""
        is_artif_ready = True
        for dept in self.get_departements():
            is_artif_ready &= dept.is_artif_ready
        return is_artif_ready

    def get_area(self) -> float:
        """Return surface of the land in Ha based on mpoly attribut."""
        return float(self.mpoly.transform(self.srid_source, clone=True).area / 10000)


class Region(AdminTerritory):
    def get_qs_cerema(self) -> QuerySet[Cerema]:
        return Cerema.objects.filter(region_id=self.official_id)


class Departement(AdminTerritory):
    """Departement contains information about OCS GE deployement and millesimes availibility."""

    is_artif_ready = models.BooleanField("Données artif disponibles", default=False)
    ocsge_millesimes = ArrayField(models.IntegerField(), null=True, blank=True)

    def get_ocsge_millesimes(self) -> set:
        return set(self.ocsge_millesimes)

    def get_qs_cerema(self) -> QuerySet[Cerema]:
        return Cerema.objects.filter(dept_id=self.official_id)


class Scot(AdminTerritory):
    def get_qs_cerema(self) -> QuerySet[Cerema]:
        return Cerema.objects.filter(city_insee__in=[city.official_id for city in self.get_cities()])


class Epci(AdminTerritory):
    def get_qs_cerema(self) -> QuerySet[Cerema]:
        return Cerema.objects.filter(epci_id=self.official_id)


class Commune(AdminTerritory):
    ocsge_available = models.BooleanField(
        "Statut de couverture OCSGE",
        default=False,
    )
    first_millesime = models.IntegerField(
        "Premier millésime disponible",
        validators=[MinValueValidator(2000), MaxValueValidator(2050)],
        blank=True,
        null=True,
    )
    last_millesime = models.IntegerField(
        "Dernier millésime disponible",
        validators=[MinValueValidator(2000), MaxValueValidator(2050)],
        blank=True,
        null=True,
    )

    def insee(self) -> str:
        """Refacto: to be removed ?"""
        return self.official_id

    def get_qs_cerema(self) -> QuerySet[Cerema]:
        return Cerema.objects.filter(city_insee=self.official_id)
