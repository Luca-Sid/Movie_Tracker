FROM mysql:latest

# Copy the initialization script into the Docker image
COPY ./init/ /docker-entrypoint-initdb.d/

EXPOSE 3306