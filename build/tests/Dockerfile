FROM python:3.7-slim-buster

RUN pip install pipenv
RUN pip install -U pytest

WORKDIR /usr/src/app

COPY Pipfile ./
COPY Pipfile.lock ./

RUN set -ex && pipenv install --deploy --system

COPY . . 

CMD sleep 4s && pytest -v