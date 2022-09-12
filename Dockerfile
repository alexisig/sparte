FROM python:3.9

LABEL maintainer="swann.bouviermuller@gmail.com"
LABEL vendor="Innov & Code"

# Setup GDAL
RUN apt update
RUN apt install -y binutils libproj-dev gdal-bin libgdal-dev

# copy all the app
COPY . ./app

WORKDIR /app

# upgrade pip
RUN pip install --upgrade pip
# install pipenv
RUN pip install pipenv
# install project dependencies
RUN pipenv install --dev --deploy --system --ignore-pipfile

EXPOSE 8080

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
