"""
Ce fichier contient les référentiels CouvertureSol et UsageSol qui sont les deux
types d'analyse fournies par l'OCSGE.
"""
from django.db import models


class BaseSol(models.Model):
    class Meta:
        abstract = True

    code_prefix = models.CharField("Nomenclature préfixée", max_length=10, unique=True)
    code = models.CharField("Nomenclature", max_length=8, unique=True)
    label = models.CharField("Libellé", max_length=250)
    map_color = models.CharField("Couleur", max_length=8, blank=True, null=True)

    @property
    def level(self) -> int:
        """Return the level of the instance in the tree
        CS1 => 1
        CS1.1 => 2
        CS1.1.1.1 => 4
        """
        return len(self.code.split("."))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cached_children = None
        self.cached_parent = None
        self.total_surface = dict()

    @property
    def children(self):
        raise NotImplementedError("Needs to be overrided")

    def get_children(self):
        """Ensure Django does not reload data from databases, therefore we can
        add some calculated data on the fly."""
        if not self.cached_children:
            self.cached_children = self.children.all()
        return self.cached_children

    @property
    def parent(self):
        raise NotImplementedError("Needs to be overrided")

    def get_parent(self):
        """Same as get_children, cache the parent to ensure django don't reload it"""
        if not self.cached_parent:
            self.cached_parent = self.parent
        return self.cached_parent

    def set_parent(self):
        """Probably useless now, calculate the parent of it.
        Example: return 'us1.2' for 'us1.2.2'
        """
        if len(self.code) < 3:
            return
        try:
            self.parent = self.__class__.objects.get(code=self.code[:-2])
            self.save()
        except self.DoesNotExist:
            return

    def __str__(self):
        return f"{self.code_prefix} {self.label}"


class UsageSol(BaseSol):
    parent = models.ForeignKey(
        "UsageSol",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="children",
    )


class CouvertureSol(BaseSol):
    parent = models.ForeignKey(
        "CouvertureSol",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="children",
    )


class CouvertureUsageMatrix(models.Model):
    class LabelChoices(models.TextChoices):
        ARTIFICIAL = "ARTIF", "Artificiel"
        CONSUMED = "CONSU", "Consommé"
        NAF = "NAF", "NAF"
        ARTIF_NOT_CONSUMED = "ARTIF_NOT_CONSU", "Artificiel non consommé"
        NONE = "NONE", "Non renseigné"

    couverture = models.ForeignKey("CouvertureSol", on_delete=models.PROTECT)
    usage = models.ForeignKey("UsageSol", on_delete=models.PROTECT)
    is_artificial = models.BooleanField("Artificiel", default=False)
    is_consumed = models.BooleanField("Consommé", default=False)
    is_natural = models.BooleanField("Naturel", default=False)
    label = models.CharField(
        "Libellé",
        max_length=20,
        choices=LabelChoices.choices,
        default=LabelChoices.NONE,
    )

    def compute(self):
        """Set is_field to correct boolean value according to label"""
        self.is_artificial = self.is_consumed = self.is_natural = False
        if self.label == self.LabelChoices.ARTIFICIAL:
            self.is_artificial = True
            self.is_consumed = True
        elif self.label == self.LabelChoices.ARTIF_NOT_CONSUMED:
            self.is_artificial = True
        elif self.label == self.LabelChoices.CONSUMED:
            self.is_consumed = True
            self.is_natural = True
        elif self.label == self.LabelChoices.NAF:
            self.is_natural = True

    def __str__(self):
        us = self.usage.code_prefix
        cs = self.couverture.code_prefix
        a = "a" if self.is_artificial else ""
        c = "c" if self.is_consumed else ""
        n = "n" if self.is_natural else ""
        return f"{cs}-{us}:{a}{c}{n}"