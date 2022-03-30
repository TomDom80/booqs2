FROM python:3.10-slim

LABEL maintainer="Tom Dom<tomdom80@gmail.com>"
LABEL description="Books 2.0"

ARG STATIC_URL
ENV STATIC_URL ${STATIC_URL:-/static/}

RUN apt-get update \
    && apt-get -y install postgresql gcc python3-dev musl-dev mc

RUN pip3 install psycopg2-binary

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8000

RUN mkdir -p /usr/src/app/media /usr/src/app/static
