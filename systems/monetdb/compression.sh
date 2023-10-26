#!/bin/sh


current="$(pwd)"
results=$( du -sk ./master_db/mydb)
result=$(echo "$results" | awk '{print $1}')
echo "${result}KB"
