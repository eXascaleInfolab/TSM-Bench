#!/bin/sh

../questdb/./questdb-6.4.1-rt-linux-amd64/bin/questdb.sh stop
fuser -k 9000/tcp


docker start clickhouse-container 
# sudo docker exec -it clickhouse-container clickhouse-client
