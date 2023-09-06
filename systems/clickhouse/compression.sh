#!/bin/sh

# THE FOLLOWING SCRIPT WILL PRINT STORAGE SIZE FOR D1, TO SHOW D2 UNCOMMENT THE LINES BELOW 

sudo docker start clickhouse-container


retries=0
while true; do
    container_status=$(sudo docker ps --format "{{.Names}}" | grep -E '^clickhouse-container$')
    if [ -n "$container_status" ]; then
        break
    fi
    retries=$((retries + 1))
    if [ "$retries" -ge "30" ]; then
        echo "Container 'clickhouse-container' did not start within the expected time."
        exit 1
    fi
    sleep 1
done
sleep 2


sudo docker exec -it clickhouse-container clickhouse-client --query "SELECT table, formatReadableSize(sum(bytes)) as size FROM system.parts WHERE active AND table='d1' GROUP BY table;"
#sudo docker exec -it clickhouse-container clickhouse-client --query "SELECT table, formatReadableSize(sum(bytes)) as size FROM system.parts WHERE active AND table='d2' GROUP BY table;"

sudo docker stop clickhouse-container
