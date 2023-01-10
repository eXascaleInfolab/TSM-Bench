#!/bin/sh

sudo docker pull timescale/timescaledb-ha:pg14-latest

sudo docker run -d --name timescaledb-container \
	-p 5433:5433 \
	-v $HOME/:/var/lib/postgresql/data \
	-e POSTGRES_PASSWORD=password timescale/timescaledb-ha:pg14-latest

sudo docker stop timescaledb-container
#  docker exec -it timescaledb psql -U postgres
#https://docs.timescale.com/install/latest/installation-docker/
