FROM python:3.7-slim-buster

RUN pip install pipenv

WORKDIR /usr/src/app

COPY Pipfile ./
COPY Pipfile.lock ./

RUN set -ex && pipenv install --deploy --system

COPY . . 

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV REDIS_DB=0

CMD python parser.py && rqscheduler --host ${REDIS_HOST} --port ${REDIS_PORT} --db ${REDIS_DB}