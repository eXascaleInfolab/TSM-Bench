#!/bin/sh

pip3 install psycopg2-binary
sudo docker pull timescale/timescaledb-ha:pg14-latest
sudo docker stop timescaledb-container
sudo docker rm timescaledb-container

ABSOLUTE_PATH=$(readlink -f "../../../")
sudo docker run -d --name timescaledb-container \
	-p 5432:5432 \
	-v $ABSOLUTE_PATH:/var/lib/postgresql/data \
	-e POSTGRES_PASSWORD=postgres \
	timescale/timescaledb-ha:pg14-latest

sudo docker start timescaledb-container

sleep 20

sudo docker cp ./pg_hba.conf  timescaledb-container:/home/postgres/pgdata/data/

sleep 10

sudo docker restart timescaledb-container

sleep 10