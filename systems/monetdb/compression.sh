#!/bin/sh

# THE FOLLOWING SCRIPT WILL PRINT STORAGE SIZE FOR D1, TO SHOW D2 UNCOMMENT THE LINES BELOW 

current="$(pwd)"
results=$(sudo du -sk ./master_db/mydb)
result=$(echo "$results" | awk '{print $1}')
echo "$result"
