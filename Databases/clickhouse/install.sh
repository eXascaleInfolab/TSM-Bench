#!/bin/sh


sudo docker pull clickhouse/clickhouse-server

sudo docker run -d --name clickhouse-container clickhouse/clickhouse-server
# sudo docker stop clickhouse-container