#!/bin/bash

# THE FOLLOWING SCRIPT WILL SETUP AND LOAD D1, TO LOAD D2 UNCOMMENT THE LINES BELOW 

dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi
echo "loading $dataset"

sed "s/d1/$dataset/g" create.sql > eXtremeDB/target/bin/create.sql
#cp create.sql eXtremeDB/target/bin

start_time=$(date +%s.%N)
cd eXtremeDB/target/bin
./xsql -b -c xsql.cfg -p 5001 -f create.sql;



end_time=$(date +%s.%N)
elapsed_time=$(echo "$end_time - $start_time" | bc)
echo "Loading time: $elapsed_time seconds" > loading_time_$dataset.txt
echo $elapsed_time
echo "database compression"
du -sh datapoints.dbs


## uncoment the following for D2 ##
###################################
# echo "start loading!"

#./xsql -b -c xsql.cfg -p 5001 -f create2.sql;
#du -sh datapoints.dbs
