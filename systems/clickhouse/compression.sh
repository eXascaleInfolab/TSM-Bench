#!/bin/sh

dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi


docker start clickhouse-container


retries=0
while true; do
    container_status=$(docker ps --format "{{.Names}}" | grep -E '^clickhouse-container$')
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


output=$(docker exec -it clickhouse-container clickhouse-client --query "SELECT table, formatReadableSize(sum(bytes)) as size FROM system.parts WHERE active AND table='$dataset' GROUP BY table;")


docker stop clickhouse-container


result=$(echo "$output" | awk '{print $2$3}'  | tr -d '\r')
echo "$result" 



