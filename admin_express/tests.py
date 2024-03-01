import pytest
from model_bakery import baker
from model_bakery.recipe import Recipe
from django.contrib.gis.geos import MultiPolygon, Polygon

from admin_express.models import AdminTerritory, Region, Departement, Scot, Epci, Commune
from public_data.models import Cerema


SMALL_SQUARE = MultiPolygon([Polygon.from_bbox((43.4, -0.6, 43.6, -0.4))], srid=4326)


region_recipe = Recipe(Region, category=AdminTerritory.CATEGORY.REGION, name=baker.seq("Région "), mpoly=SMALL_SQUARE)


departement_recipe = Recipe(
    Departement, category=AdminTerritory.CATEGORY.DEPARTEMENT, name=baker.seq("Département "), mpoly=SMALL_SQUARE
)


scot_recipe = Recipe(Scot, category=AdminTerritory.CATEGORY.SCOT, name=baker.seq("SCoT "), mpoly=SMALL_SQUARE)


epci_recipe = Recipe(Epci, category=AdminTerritory.CATEGORY.EPCI, name=baker.seq("EPCI "), mpoly=SMALL_SQUARE)


commune_recipe = Recipe(
    Commune, category=AdminTerritory.CATEGORY.COMMUNE, name=baker.seq("Commune "), mpoly=SMALL_SQUARE
)


@pytest.fixture()
def db_small_setup(db):
    dept = departement_recipe.make(official_id="10", is_artif_ready=True, ocsge_millesimes=[2018, 2020])
    comm = commune_recipe.make(
        official_id="10100", ocsge_available=True, first_millesime=2018, last_millesime=2020, parents=[dept]
    )
    commune_recipe.make(official_id="10101", parents=[dept])
    return comm, dept


@pytest.fixture()
def db_setup(db, db_small_setup) -> tuple[Commune, Epci, Scot, Departement, Region]:  # noqa: F811
    comm: Commune
    dept: Departement
    comm, dept = db_small_setup

    region = region_recipe.make(official_id="05")
    dept2 = departement_recipe.make(official_id="11", ocsge_millesimes=[2019, 2020])
    scot = scot_recipe.make(official_id="11122233345678", parents=[dept, dept2])
    epci = epci_recipe.make(official_id="45678912300012", parents=[dept, scot])

    commune_recipe.make(official_id="10103", parents=[dept2])

    comm.parents.add(epci)
    comm.parents.add(scot)
    comm.parents.add(region)
    dept.parents.add(region)

    return comm, epci, scot, dept, region


@pytest.fixture()
def db_cerema(db, db_small_setup) -> "Cerema":
    comm, dept = db_small_setup
    cerema_dept = baker.make("public_data.Cerema", _quantity=3, dept_id=dept.official_id)
    cerema_dept.append(baker.make("public_data.Cerema", city_insee=comm.official_id))
    return cerema_dept


@pytest.mark.django_db
class TestManager:
    def test_force_subclasses(self, db_small_setup):
        instance = AdminTerritory.objects.all().first()
        assert isinstance(instance, Departement)

    def test_trasnform_into_communes(self, db_small_setup):
        qs = AdminTerritory.objects.filter(category=AdminTerritory.CATEGORY.DEPARTEMENT)
        assert qs.get_communes().count() == 2
        assert list(Commune.objects.all()) == list(qs.communes())


@pytest.mark.django_db
class TestTerritories:
    def test_parents_and_children(self, db_setup):
        comm = AdminTerritory.objects.get(official_id="10100")
        assert comm.parents.all().count() == 4

    def test_linked_territory(self, db_setup):
        comm = AdminTerritory.objects.get(official_id="10100")
        assert list(comm.get_scots()) == [db_setup[2]]
        assert comm.get_scot() == db_setup[2]
        scot = Scot.objects.get(official_id="11122233345678")
        depts = Departement.objects.filter(official_id__in=[10, 11])
        assert list(scot.get_departements()) == list(depts)
        with pytest.raises(AdminTerritory.MultipleObjectsReturned):
            scot.get_departement()

    def test_get_ocsge_millesimes(self, db_setup):
        single_dept = {2018, 2020}
        double_dept = {2018, 2019, 2020}
        dept = Departement.objects.get(official_id="10")
        assert dept.get_ocsge_millesimes() == single_dept
        dept = AdminTerritory.objects.get(official_id="11")
        assert dept.get_ocsge_millesimes() == {2019, 2020}
        region = Region.objects.get(official_id="05")
        assert region.get_ocsge_millesimes() == single_dept
        scot = Scot.objects.get(official_id="11122233345678")
        assert scot.get_ocsge_millesimes() == double_dept
        epci = Epci.objects.get(official_id="45678912300012")
        assert epci.get_ocsge_millesimes() == single_dept
        comm = Commune.objects.get(official_id="10100")
        assert comm.get_ocsge_millesimes() == single_dept

    def test_cerema(self, db_cerema):
        with pytest.raises(NotImplementedError):
            AdminTerritory().get_qs_cerema()
        comm = Commune.objects.get(official_id="10100")
        dept = Departement.objects.get(official_id="10")
        assert Cerema.objects.all().count() == 4
        assert dept.get_qs_cerema().count() == 3
        assert comm.get_qs_cerema().count() == 1

    def test_commune_insee(self, db_small_setup):
        comm, dept = db_small_setup
        assert comm.insee() == comm.official_id

    def test_is_artif_ready(self, db_setup):
        # single departement linked with artif ready
        assert Commune.objects.get(official_id="10100").is_artif_ready() is True
        assert Region.objects.get(official_id="05").is_artif_ready() is True
        assert Epci.objects.get(official_id="45678912300012").is_artif_ready() is True
        # 2 departements linked with different artif ready
        assert Scot.objects.get(official_id="11122233345678").is_artif_ready() is False
