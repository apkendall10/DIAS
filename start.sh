#!/bin/bash

# creates a container for both worker and manager
docker-compose -f "docker/docker-compose.yml" up -d

# app="worker"
# docker build -t ${app} docker/
# docker run -d -p 8002:80 \
#   --name=${app} \
#   -v "$PWD/worker:/app" ${app}