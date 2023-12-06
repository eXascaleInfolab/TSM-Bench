#!/bin/sh

# THE FOLLOWING SCRIPT WILL PRINT STORAGE SIZE FOR D1, TO SHOW D2 UNCOMMENT THE LINES BELOW 

dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi

result=$(du -sk ./apache-druid-25.0.0/var/druid/segment-cache/$dataset)
result=$(echo "$result" | awk '{print $1}')
echo "${result}KB"
