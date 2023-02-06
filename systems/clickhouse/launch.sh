#!/bin/sh

sudo kill -9 `sudo lsof -t -i:9000`
sudo docker start clickhouse-container
# sudo docker exec -it clickhouse-container clickhouse-client
