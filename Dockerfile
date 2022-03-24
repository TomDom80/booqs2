FROM python:3.10-alpine

ARG STATIC_URL
ENV STATIC_URL ${STATIC_URL:-/static/}
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
EXPOSE 8000
