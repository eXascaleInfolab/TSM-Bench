#!/bin/sh

sudo docker start timescaledb-container

sudo docker exec -it timescaledb-container psql -U postgres -c "SELECT hypertable_size('d1') ;";

sudo docker stop timescaledb-container