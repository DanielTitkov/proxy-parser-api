FROM python:3.7-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

ENV APIPORT=8000
ENV WORKERS=3

CMD gunicorn --bind 0.0.0.0:${APIPORT} --workers=${WORKERS} server:app 