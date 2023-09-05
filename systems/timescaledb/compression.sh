#!/bin/sh

# THE FOLLOWING SCRIPT WILL PRINT STORAGE SIZE FOR D1, TO SHOW D2 UNCOMMENT THE LINES BELOW 

sudo docker start timescaledb-container


sleep 15

sudo docker exec -it timescaledb-container psql -U postgres -c "SELECT hypertable_size('d1') ;";
#sudo docker exec -it timescaledb-container psql -U postgres -c "SELECT hypertable_size('d2') ;";

sudo docker stop timescaledb-container
