#!/bin/sh

sudo docker pull timescale/timescaledb-ha:pg14-latest

sudo docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb-ha:pg14-latest

#  docker exec -it timescaledb psql -U postgres
#https://docs.timescale.com/install/latest/installation-docker/