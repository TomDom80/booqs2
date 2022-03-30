FROM nginx:1.19.0-alpine
RUN apk update && apk add mc
RUN mkdir /app
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/
WORKDIR /app