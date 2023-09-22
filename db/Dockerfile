FROM postgres:latest
ENV POSTGRES_PASSWORD=secret
ENV POSTGRES_USER=username
ENV POSTGRES_DB=database
COPY init_db.sql /docker-entrypoint-initdb.d/init_db.sql
