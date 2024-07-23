import os

from airflow.operators.empty import EmptyOperator
from airflow.operators.python_operator import PythonOperator

from airflow import DAG

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


def my_callable(*args, **kwargs):
    from geopandas import show_versions

    show_versions()


with DAG(
    "test_dag",
    schedule_interval="@once",
) as dag:
    download_ocsge_7z_file_task = EmptyOperator(task_id="download_ocsge_7z_file")
    unzip_ocsge_7z_to_shapefile_task = EmptyOperator(task_id="unzip_ocsge_7z_file")
    create_geopackage_from_ocsge_shapefile = EmptyOperator(task_id="repack_ocsge_shapefile_to_geopackage")
    add_additionnal_fields_to_geopackage_task = EmptyOperator(task_id="add_additionnal_fields_to_geopackage")
    test_operator = PythonOperator(task_id="test_operator", python_callable=my_callable)
