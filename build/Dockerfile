FROM python:3.7-slim-buster

RUN pip install pipenv
RUN pip install -U pytest
# RUN if [ X"$TEST" = "true" ]; then echo "TRUE" && pip install -U pytest; fi

WORKDIR /usr/src/app

COPY Pipfile ./
COPY Pipfile.lock ./

RUN set -ex && pipenv install --deploy --system

COPY . .