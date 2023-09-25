#!/bin/bash

# THE FOLLOWING SCRIPT WILL SETUP AND LOAD D1, TO LOAD D2 UNCOMMENT THE LINES BELOW 

start_time=$(date +%s.%N)
cd eXtremeDB/target/bin
./xsql -b -c xsql.cfg -p 5001 -f create.sql;


end_time=$(date +%s.%N)

# Calculate the time taken in seconds
elapsed_time=$(echo "$end_time - $start_time" | bc)


du -sh datapoints.dbs


## uncoment the following for D2 ##
###################################
# echo "start loading!"

#./xsql -b -c xsql.cfg -p 5001 -f create2.sql;
#du -sh datapoints.dbs
