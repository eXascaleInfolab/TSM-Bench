#!/bin/sh


sudo kill -9 `sudo lsof -t -i:9000`
sleep 2

pip3 install clickhouse-driver

sudo docker pull clickhouse/clickhouse-server

# Run the ClickHouse container
docker run -d --name clickhouse-container   -p 8123:8123 -p 9000:9000  -v $(pwd)/clickhouse-config.xml:/etc/clickhouse-server/config.xml  clickhouse/clickhouse-server

sleep 5
sudo docker stop clickhouse-container



