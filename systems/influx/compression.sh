#!/bin/sh

# THE FOLLOWING SCRIPT WILL PRINT STORAGE SIZE FOR D1, TO SHOW D2 UNCOMMENT THE LINES BELOW 
dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi
output=$(sudo du -sh /var/lib/influxdb/data/$dataset)
result=$(echo "$output" | awk '{print $1}')

echo "$result"
