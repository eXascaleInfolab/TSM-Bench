#!/bin/sh

docker stop clickhouse-container

system_directory="$HOME/.questdb" # change this if needed

./questdb-6.4.1-rt-linux-amd64/bin/questdb.sh start -d "$system_directory"

# http:localhost:9000
