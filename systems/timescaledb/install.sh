#!/bin/sh

pip3 install psycopg2-binary

sudo docker pull timescale/timescaledb-ha:pg14-latest

sudo docker stop timescaledb-container
sudo docker rm timescaledb-container


ABSOLUTE_PATH=$(readlink -f "../../../")

sudo docker run -d --name timescaledb-container \
	-p 127.0.0.1:5431:5432 \
	-v $ABSOLUTE_PATH:/var/lib/postgresql/data \
	-e POSTGRES_PASSWORD=postgres \
	timescale/timescaledb-ha:pg14-latest


#  docker exec -it timescaledb psql -U postgres
#https://docs.timescale.com/install/latest/installation-docker/


sudo docker start timescaledb-container
#sudo docker exec -it timescaledb-container psql -U postgres
sleep 5


sh load.sh


