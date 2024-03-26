FROM mysql:8.0

WORKDIR /docker-entrypoint-initdb.d
COPY ./initdb .

EXPOSE 3306

ENV MYSQL_ROOT_PASSWORD=142536
ENV MYSQL_DATABASE=mvp2
ENV MYSQL_USER=app
ENV MYSQL_PASSWORD=app142536
ENV MYSQL_INIT_DB=/docker-entrypoint-initdb.d/init.sql