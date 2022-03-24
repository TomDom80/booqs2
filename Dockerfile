FROM python:3.10-alpine
LABEL maintainer="Tom Dom<tomdom80@gmail.com>"
LABEL description="Books 2.0"
ARG STATIC_URL
ENV STATIC_URL ${STATIC_URL:-/static/}
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk update
RUN apk add
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
EXPOSE 8000
