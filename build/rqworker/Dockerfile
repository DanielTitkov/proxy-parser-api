FROM python:3.7-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV REDIS_DB=0

CMD rq worker --url=redis://${REDIS_HOST}:${REDIS_PORT}/${REDIS_DB} high default low 