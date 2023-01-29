#!/bin/sh

pip3 install psycopg2-binary

sudo docker pull timescale/timescaledb-ha:pg14-latest

sudo docker run -d --name timescaledb-container \
	-p 127.0.0.1:5432:5432 \
	-v $HOME/:/var/lib/postgresql/data \
	-e POSTGRES_PASSWORD=postgres \
	timescale/timescaledb-ha:pg14-latest

sudo docker stop timescaledb-container
#  docker exec -it timescaledb psql -U postgres
#https://docs.timescale.com/install/latest/installation-docker/
