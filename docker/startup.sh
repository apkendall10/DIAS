docker run -d --name=worker worker
docker run -d -p 8002:80 --name=manager manager
