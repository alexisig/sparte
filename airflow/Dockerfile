FROM apache/airflow:2.9.3-python3.11

# Setup GDAL
USER root
RUN apt update
RUN apt-get install --reinstall build-essential -y
RUN apt install -y binutils libproj-dev gdal-bin libgdal-dev

# upgrade pip
USER airflow

RUN pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile.lock Pipfile ./
RUN pipenv requirements > requirements.txt
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r requirements.txt


# install project dependencies
