#!/bin/sh
sudo docker stop clickhouse-container
sudo kill -9 `sudo lsof -t -i:9000`
sleep 5
sudo docker start clickhouse-container
# sudo docker exec -it clickhouse-container clickhouse-client
