#!/bin/sh

sudo docker run -p 9000:9000 \
-p 9009:9009 \
-p 8812:8812 \
-p 9003:9003 \
-v "$(pwd):/var/lib/questdb" \
questdb/questdb:6.6.1

# https://questdb.io/docs/get-started/docker/