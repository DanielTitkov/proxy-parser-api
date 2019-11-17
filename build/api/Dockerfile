FROM python:3.7-slim-buster

RUN pip install pipenv

WORKDIR /usr/src/app

COPY Pipfile ./
COPY Pipfile.lock ./

RUN set -ex && pipenv install --deploy --system

COPY . . 

ENV APIPORT=8000
ENV WORKERS=3

CMD gunicorn --bind 0.0.0.0:${APIPORT} --workers=${WORKERS} server:app 