#!/bin/sh

. ../config.env

docker stop clickhouse-container

./questdb-6.2.1-rt-linux-amd64/bin/questdb.sh start -d "$QuestDBroot"

# http:localhost:9000
