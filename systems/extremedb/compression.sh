#!/bin/sh

# THE FOLLOWING SCRIPT WILL PRINT STORAGE SIZE FOR D1, TO SHOW D2 UNCOMMENT THE LINES BELOW 

output=$(sudo du -sk eXtremeDB/target/bin/datapoints.dbs)
echo "$output"
compression=$(echo "$output" | awk '{print $1}')
echo "$compression"
