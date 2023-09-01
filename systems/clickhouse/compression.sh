#!/bin/sh

# THE FOLLOWING SCRIPT WILL SETUP AND LOAD D1, TO LOAD D2 UNCOMMENT THE LINES BELOW 

sudo docker start clickhouse-container

sudo docker exec -it clickhouse-container clickhouse-client --query "SELECT table, formatReadableSize(sum(bytes)) as size FROM system.parts WHERE active AND table='d1' GROUP BY table;"
#sudo docker exec -it clickhouse-container clickhouse-client --query "SELECT table, formatReadableSize(sum(bytes)) as size FROM system.parts WHERE active AND table='d2' GROUP BY table;"

sudo docker stop clickhouse-container
