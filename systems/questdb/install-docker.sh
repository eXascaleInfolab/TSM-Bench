#!/bin/sh

docker stop questdb-container
docker rm questdb-container 
docker pull questdb/questdb:6.6.1
docker run -d -p 9000:9000 \
        --name questdb-container \
        -v "$pwd:/var/lib/questdb" \
        questdb/questdb:6.6.1
docker stop questdb-container

