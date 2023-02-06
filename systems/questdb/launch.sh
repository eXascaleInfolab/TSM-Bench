#!/bin/sh

sudo kill -9 `sudo lsof -t -i:9000`
sudo docker stop clickhouse-container
sudo ./questdb-6.4.1-rt-linux-amd64/bin/questdb.sh start

# http://diufrm108:9000
