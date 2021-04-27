#!/bin/bash

docker build -t worker ./worker
docker build -t manager ./manager
docker run -d --name=worker -p 8007:80 worker
docker run -d --name=manager -p 8002:80 manager