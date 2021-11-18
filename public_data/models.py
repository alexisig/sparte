from decimal import Decimal

from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Area, Transform
from django.db import models as classic_models


from .behaviors import AutoLoadMixin, DataColorationMixin


class ArtifCommune(classic_models.Model):
    name = classic_models.CharField("Nom", max_length=250)
    insee = classic_models.CharField("Code INSEE", max_length=10)
    surface = classic_models.DecimalField(
        "surface (ha)", max_digits=8, decimal_places=2
    )
    artif_before_2009 = classic_models.DecimalField(
        "Artificial before 2009 (ha)", max_digits=8, decimal_places=2
    )
    artif_2009 = classic_models.DecimalField(
        "New artificial 2009 (ha)", max_digits=8, decimal_places=2
    )
    artif_2010 = classic_models.DecimalField(
        "New artificial 2010 (ha)", max_digits=8, decimal_places=2
    )
    artif_2011 = classic_models.DecimalField(
        "New artificial 2011 (ha)", max_digits=8, decimal_places=2
    )
    artif_2012 = classic_models.DecimalField(
        "New artificial 2012 (ha)", max_digits=8, decimal_places=2
    )
    artif_2013 = classic_models.DecimalField(
        "New artificial 2013 (ha)", max_digits=8, decimal_places=2
    )
    artif_2014 = classic_models.DecimalField(
        "New artificial 2014 (ha)", max_digits=8, decimal_places=2
    )
    artif_2015 = classic_models.DecimalField(
        "New artificial 2015 (ha)", max_digits=8, decimal_places=2
    )
    artif_2016 = classic_models.DecimalField(
        "New artificial 2016 (ha)", max_digits=8, decimal_places=2
    )
    artif_2017 = classic_models.DecimalField(
        "New artificial 2017 (ha)", max_digits=8, decimal_places=2
    )
    artif_2018 = classic_models.DecimalField(
        "New artificial 2018 (ha)", max_digits=8, decimal_places=2
    )

    @classmethod
    def list_attr(cls):
        return ["artif_before_2009"] + [f"artif_{y}" for y in range(2009, 2019)]

    def list_artif(self, flat=True):
        val = {f: getattr(self, f, 0.0) for f in self.__class__.list_attr()}
        if flat:
            return val.values()
        return val

    def total_artif(self):
        return sum(self.list_artif())

    def total_percent(self, decimal=False):
        val = self.total_artif() / self.surface
        if not decimal:
            return val
        else:
            return Decimal(val)

    def percent(self, name, decimal=False):
        val = getattr(self, name, 0.0) / self.surface
        if not decimal:
            return val
        else:
            return Decimal(val)

    def list_percent(self, decimal=False):
        val = (_ / self.surface for _ in self.list_artif())
        if not decimal:
            return val
        else:
            return map(Decimal, val)

    def __str__(self):
        return f"{self.name} - {self.insee}"


class CommunesSybarval(models.Model, AutoLoadMixin, DataColorationMixin):
    """
    Communes_SYBARVAL : les communes avec les même attributs
    Données produites par Philippe
    """

    id_source = models.CharField("id", max_length=24)
    prec_plani = models.FloatField("prec_plani", max_length=6)
    nom = models.CharField("Nom", max_length=45)
    code_insee = models.CharField("Code INSEE", max_length=5)
    statut = models.CharField("statut", max_length=22)
    arrondisst = models.CharField("arrondisst", max_length=45)
    depart = models.CharField("departement", max_length=30)
    region = models.CharField("region", max_length=35)
    pop_2014 = models.IntegerField("Population 2014")
    pop_2015 = models.IntegerField("Population 2015")
    _commune = models.CharField("Commune", max_length=254)
    _n_arrdt = models.IntegerField("nb arrdt")
    _n_canton = models.IntegerField("nb cantons")
    _nom_epci = models.CharField("Nom EPCI", max_length=254)
    _siren_epc = models.IntegerField("siren epc")
    _nom_scot = models.CharField("Nom SCOT", max_length=254)
    surface = models.IntegerField("Surface")
    a_brute_20 = models.IntegerField("a_brute_20")
    a_b_2015_2 = models.IntegerField("a_b_2015_2")
    a_b_2018_2 = models.IntegerField("a_b_2018_2")
    z_baties_2 = models.IntegerField("z_baties_2")
    voirie_201 = models.IntegerField("voirie_201")
    tache_2018 = models.IntegerField("tache_2018")
    d_brute_20 = models.FloatField("d_brute_20")
    d_batie_20 = models.FloatField("d_batie_20")
    d_voirie_2 = models.FloatField("d_voirie_2")

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    shape_file_path = "communes_sybarval.zip"
    default_property = "surface"
    default_color = "Yellow"
    mapping = {
        "id_source": "ID",
        "prec_plani": "PREC_PLANI",
        "nom": "NOM",
        "code_insee": "CODE_INSEE",
        "statut": "STATUT",
        "arrondisst": "ARRONDISST",
        "depart": "DEPART",
        "region": "REGION",
        "pop_2014": "Pop_2014",
        "_commune": "_Commune",
        "pop_2015": "Pop_2015",
        "_n_arrdt": "_N_arrdt",
        "_n_canton": "_N_canton",
        "_nom_epci": "_Nom_EPCI",
        "_siren_epc": "_SIREN_EPC",
        "_nom_scot": "_Nom_ScoT",
        "surface": "Surface",
        "a_brute_20": "A_Brute_20",
        "a_b_2015_2": "A_B_2015_2",
        "a_b_2018_2": "A_B_2018_2",
        "z_baties_2": "Z_Baties_2",
        "voirie_201": "Voirie_201",
        "tache_2018": "Tache_2018",
        "d_brute_20": "D_Brute_20",
        "d_batie_20": "D_Batie_20",
        "d_voirie_2": "D_Voirie_2",
        "mpoly": "MULTIPOLYGON",
    }

    # Returns the string representation of the model.
    def __str__(self):
        return self.nom


class Artificialisee2015to2018(models.Model, AutoLoadMixin, DataColorationMixin):
    """
    A_B_2015_2018 : la surface (en hectares) artificialisée entre 2015 et 2018
    Données construites par Philippe
    """

    surface = models.IntegerField("surface")
    cs_2018 = models.CharField("Couverture 2018", max_length=254, null=True)
    us_2018 = models.CharField("Usage 2018", max_length=254, null=True)
    cs_2015 = models.CharField("Couverture 2015", max_length=254, null=True)
    us_2015 = models.CharField("Usage 2015", max_length=254, null=True)

    # calculated fields
    cs_2018_label = models.CharField(
        "Couverture 2018", max_length=254, blank=True, null=True
    )
    us_2018_label = models.CharField(
        "Usage 2018", max_length=254, blank=True, null=True
    )
    cs_2015_label = models.CharField(
        "Couverture 2015", max_length=254, blank=True, null=True
    )
    us_2015_label = models.CharField(
        "Usage 2015", max_length=254, blank=True, null=True
    )

    mpoly = models.MultiPolygonField()

    shape_file_path = "a_b_2015_2018.zip"
    default_property = "surface"
    default_color = "Red"
    mapping = {
        "surface": "Surface",
        "cs_2018": "cs_2018",
        "us_2018": "us_2018",
        "cs_2015": "cs_2015",
        "us_2015": "us_2015",
        "mpoly": "MULTIPOLYGON",
    }

    @classmethod
    def calculate_fields(cls):
        """override to hook specific label setting."""
        cls.set_labels()

    @classmethod
    def set_labels(cls):
        """Set label for cs and us fields."""
        for fieldname in ["cs_2018", "us_2018", "cs_2015", "us_2015"]:
            if fieldname.startswith("cs"):
                cls.set_label(CouvertureSol, fieldname, f"{fieldname}_label")
            else:
                cls.set_label(UsageSol, fieldname, f"{fieldname}_label")


class Renaturee2018to2015(models.Model, AutoLoadMixin, DataColorationMixin):
    """
    A_B_2018_2015 : la surface (en hectares) re-naturée entre 2018 et 2015
    Données produites par Philippe
    """

    surface = models.IntegerField("Surface")
    cs_2018 = models.CharField("Couverture 2018", max_length=254, null=True)
    us_2018 = models.CharField("Usage 2018", max_length=254, null=True)
    cs_2015 = models.CharField("Couverture 2015", max_length=254, null=True)
    us_2015 = models.CharField("Usage 2015", max_length=254, null=True)

    # calculated fields
    cs_2018_label = models.CharField(
        "Couverture 2018", max_length=254, blank=True, null=True
    )
    us_2018_label = models.CharField(
        "Usage 2018", max_length=254, blank=True, null=True
    )
    cs_2015_label = models.CharField(
        "Couverture 2015", max_length=254, blank=True, null=True
    )
    us_2015_label = models.CharField(
        "Usage 2015", max_length=254, blank=True, null=True
    )

    mpoly = models.MultiPolygonField()

    shape_file_path = "a_b_2018_2015.zip"
    default_property = "surface"
    default_color = "Lime"
    mapping = {
        "surface": "Surface",
        "cs_2018": "cs_2018",
        "us_2018": "us_2018",
        "cs_2015": "cs_2015",
        "us_2015": "us_2015",
        "mpoly": "MULTIPOLYGON",
    }

    @classmethod
    def calculate_fields(cls):
        """override to hook specific label setting."""
        cls.set_labels()

    @classmethod
    def set_labels(cls):
        """Set label for cs and us fields."""
        for fieldname in ["cs_2018", "us_2018", "cs_2015", "us_2015"]:
            if fieldname.startswith("cs"):
                cls.set_label(CouvertureSol, fieldname, f"{fieldname}_label")
            else:
                cls.set_label(UsageSol, fieldname, f"{fieldname}_label")

    @classmethod
    def get_groupby_couverture(cls, geom):
        """Return SUM(surface) GROUP BY couverture if coveredby geom.
        Return [
            {
                "couverture": "1.1.1",
                "total_surface": 678,
            },
        ]
        """
        qs = cls.objects.filter(mpoly__coveredby=geom)
        qs = qs.annotate(couverture=classic_models.F("cs_2018"))
        qs = qs.values("couverture").order_by("couverture")
        qs = qs.annotate(total_surface=classic_models.Sum("surface"))
        return qs


class Artificielle2018(models.Model, AutoLoadMixin, DataColorationMixin):
    """
    A_Brute_2018 : la surface artificialisée en hectare
    Données produites par Philippe
    """

    couverture = models.CharField("Couverture", max_length=254)
    surface = models.IntegerField("Surface")

    # Calculated fields
    couverture_label = models.CharField(
        "Libellé couverture du sol", max_length=254, blank=True, null=True
    )

    mpoly = models.MultiPolygonField()

    shape_file_path = "A_Brute_2018.zip"
    default_property = "surface"
    default_color = "Orange"
    couverture_field = "couverture"
    mapping = {
        "couverture": "couverture",
        "surface": "Surface",
        "mpoly": "MULTIPOLYGON",
    }

    @classmethod
    def get_groupby_couverture(cls, geom):
        """Return SUM(surface) GROUP BY couverture if coveredby geom.
        Return [
            {
                "couverture": "1.1.1",
                "total_surface": 678,
            },
        ]
        """
        qs = cls.objects.filter(mpoly__coveredby=geom)
        qs = qs.values("couverture").order_by("couverture")
        qs = qs.annotate(total_surface=classic_models.Sum("surface"))
        return qs


class EnveloppeUrbaine2018(models.Model, AutoLoadMixin, DataColorationMixin):
    """
    Enveloppe_Urbaine_2018 : enveloppe urbaine sans la voirie avec moins d'attributs
    """

    couverture = models.CharField("Couverture", max_length=254, null=True)
    surface = models.IntegerField("Surface")
    a_brute_20 = models.IntegerField("a_brute_20", null=True)
    z_batie_20 = models.IntegerField("z_batie_20", null=True)
    d_brute_20 = models.FloatField("d_brute_20", null=True)
    d_batie_20 = models.FloatField("d_batie_20", null=True)

    mpoly = models.MultiPolygonField()

    # calculated fields
    couverture_label = models.CharField(
        "Libellé couverture du sol", max_length=254, blank=True, null=True
    )

    shape_file_path = "Enveloppe_urbaine.zip"
    default_property = "surface"
    default_color = "Coraile"
    couverture_field = "couverture"
    mapping = {
        "couverture": "couverture",
        "surface": "Surface",
        "a_brute_20": "A_Brute_20",
        "z_batie_20": "Z_Batie_20",
        "d_brute_20": "D_Brute_20",
        "d_batie_20": "D_Batie_20",
        "mpoly": "MULTIPOLYGON",
    }


class Voirie2018(models.Model, AutoLoadMixin, DataColorationMixin):
    """
    Voirie_2018 : les objets avec leur surface
    """

    couverture = models.CharField("Couverture", max_length=254, null=True)
    usage = models.CharField("Usage", max_length=254, null=True)
    surface = models.IntegerField("Surface")

    mpoly = models.MultiPolygonField()

    # calculated fields
    couverture_label = models.CharField(
        "Libellé couverture du sol", max_length=254, blank=True, null=True
    )
    usage_label = models.CharField(
        "Libellé usage du sol", max_length=254, blank=True, null=True
    )

    shape_file_path = "Voirire_2018.zip"
    default_property = "surface"
    default_color = "Black"
    couverture_field = "couverture"
    usage_field = "usage"
    mapping = {
        "couverture": "couverture",
        "usage": "usage",
        "surface": "Surface",
        "mpoly": "MULTIPOLYGON",
    }


class ZonesBaties2018(models.Model, AutoLoadMixin, DataColorationMixin):
    """
    Zones_Baties_2018 : les objets avec leur surface
    Données produites par Philippe
    """

    couverture = models.CharField("Couverture", max_length=254, null=True)
    usage = models.CharField("Usage", max_length=254, null=True)
    surface = models.IntegerField("Surface")

    mpoly = models.MultiPolygonField()

    # calculated fields
    couverture_label = models.CharField(
        "Libellé couverture du sol", max_length=254, blank=True, null=True
    )
    usage_label = models.CharField(
        "Libellé usage du sol", max_length=254, blank=True, null=True
    )

    shape_file_path = "zones_baties_2018.zip"
    default_property = "surface"
    default_color = "Pink"
    couverture_field = "couverture"
    usage_field = "usage"
    mapping = {
        "couverture": "couverture",
        "usage": "usage",
        "surface": "Surface",
        "mpoly": "MULTIPOLYGON",
    }


class Sybarval(models.Model, AutoLoadMixin, DataColorationMixin):
    """
    SYBARVAL : les contours et les attributs utiles (seulement pour 2018) :
        - Surface en hectare
        - A_Brute_2018 : la surface artificialisée en hectare
        - A_B_2015_2018 : la surface (en hectares) artificialisée entre 2015 et 2018
        - A_B_2018_2015 : la surface (en hectares) re-naturée entre 2018 et 2015
        - Z_Baties_2018 : la surface bâtie en hectares
        - Voirie_2018 : la surface de voirie en hectares
        - Tache_2018 : la surface en hectares de l'enveloppe urbaine 2018
        - D_Brute_2018, D_Batie_2018 et D_Voirie_2018 : les densités
    Données produites par Philippe
    """

    surface = models.IntegerField("Surface")
    a_brute_20 = models.IntegerField("a_brute_20", null=True)
    a_b_2015_2 = models.IntegerField("a_b_2015_2", null=True)
    a_b_2018_2 = models.IntegerField("a_b_2018_2", null=True)
    z_baties_2 = models.IntegerField("z_baties_2", null=True)
    voirie_201 = models.IntegerField("voirie_201", null=True)
    tache_2018 = models.IntegerField("tache_2018", null=True)
    d_brute_20 = models.FloatField("d_brute_20", null=True)
    d_batie_20 = models.FloatField("d_batie_20", null=True)
    d_voirie_2 = models.FloatField("d_voirie_2", null=True)

    mpoly = models.MultiPolygonField()

    shape_file_path = "Sybarval.zip"
    default_property = "surface"
    default_color = None
    mapping = {
        "surface": "Surface",
        "a_brute_20": "A_Brute_20",
        "a_b_2015_2": "A_B_2015_2",
        "a_b_2018_2": "A_B_2018_2",
        "z_baties_2": "Z_Baties_2",
        "voirie_201": "Voirie_201",
        "tache_2018": "Tache_2018",
        "d_brute_20": "D_Brute_20",
        "d_batie_20": "D_Batie_20",
        "d_voirie_2": "D_voirie_2",
        "mpoly": "MULTIPOLYGON",
    }


class BaseSol(classic_models.Model):
    class Meta:
        abstract = True

    code_prefix = classic_models.CharField(
        "Nomenclature préfixée", max_length=10, unique=True
    )
    code = classic_models.CharField("Nomenclature", max_length=8, unique=True)
    label = classic_models.CharField("Libellé", max_length=250)

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
    parent = classic_models.ForeignKey(
        "UsageSol",
        blank=True,
        null=True,
        on_delete=classic_models.PROTECT,
        related_name="children",
    )


class CouvertureSol(BaseSol):
    parent = classic_models.ForeignKey(
        "CouvertureSol",
        blank=True,
        null=True,
        on_delete=classic_models.PROTECT,
        related_name="children",
    )
    is_artificial = classic_models.BooleanField("Est artificielle", default=False)


class BaseOcsge(models.Model, AutoLoadMixin, DataColorationMixin):
    couverture = models.CharField(
        "Couverture du sol", max_length=254, blank=True, null=True
    )
    usage = models.CharField("Usage du sol", max_length=254, blank=True, null=True)
    millesime = models.DateField("Millésime", blank=True, null=True)
    source = models.CharField("Source", max_length=254, blank=True, null=True)
    origine = models.CharField("Origine", max_length=254, blank=True, null=True)
    origine2 = models.CharField("Origine1", max_length=254, blank=True, null=True)
    ossature = models.IntegerField("Ossature", blank=True, null=True)
    commentaire = models.CharField("Commentaire", max_length=254, blank=True, null=True)

    # calculated fields
    couverture_label = models.CharField(
        "Libellé couverture du sol", max_length=254, blank=True, null=True
    )
    usage_label = models.CharField(
        "Libellé usage du sol", max_length=254, blank=True, null=True
    )
    map_color = models.CharField("Couleur", max_length=8, blank=True, null=True)

    mpoly = models.MultiPolygonField()

    default_property = "id"
    couverture_field = "couverture"
    usage_field = "usage"
    mapping = {
        "couverture": "couverture",
        "usage": "usage",
        "millesime": "millesime",
        "source": "source",
        "origine": "origine",
        "origine2": "origine2",
        "ossature": "ossature",
        "commentaire": "commentair",
        "mpoly": "MULTIPOLYGON",
    }

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["couverture"]),
            models.Index(fields=["usage"]),
        ]

    @classmethod
    def get_groupby(cls, field_group_by, coveredby):
        """Return SUM(surface) GROUP BY couverture if coveredby geom.
        Return {
            "CS1.1.1": 678,
            "CS1.1.2": 419,
        }

        Parameters:
        ==========
        * field_group_by: 'couverture' or 'usage'
        * coveredby: polynome of the perimeter in which Ocsge items mut be
        """
        qs = cls.objects.filter(mpoly__coveredby=coveredby)
        qs = qs.annotate(surface=Area(Transform("mpoly", 2154)))
        qs = qs.values(field_group_by).order_by(field_group_by)
        qs = qs.annotate(total_surface=classic_models.Sum("surface"))
        data = {_[field_group_by]: _["total_surface"].sq_km for _ in qs}
        return data


class Ocsge2015(BaseOcsge):
    """
    Données de l'OCSGE pour l'année 2015
    Données fournies par Philippe 09/2021
    python manage.py load_data --class public_data.models.Ocsge2015
    """

    shape_file_path = "OCSGE_2015.zip"
    default_color = "Chocolate"


class Ocsge2018(BaseOcsge):
    """
    Données de l'OCSGE pour l'année 2018
    Données fournies par Philippe 09/2021
    Les données sont stockés zippés dans s3://{bucket_name}/data
    Pour les charger dans la base, exécuter la commande suivante:
    python manage.py load_data --class public_data.models.Ocsge2015
    """

    shape_file_path = "OCSGE_2018.zip"
    default_color = "DarkSeaGreen"