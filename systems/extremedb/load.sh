#!/bin/bash

# THE FOLLOWING SCRIPT WILL SETUP AND LOAD D1, TO LOAD D2 UNCOMMENT THE LINES BELOW 

dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi
echo "loading $dataset into extremedb"


current="$(pwd)"

export MCO_ROOT="$current"
export MCO_LIBRARY_PATH="$current"/eXtremeDB/target/bin.so
export LD_LIBRARY_PATH="$current"/eXtremeDB/target/bin.so

# replace d1 with the specific dataset name
sed "s/d1/$dataset/g" create.sql > eXtremeDB/target/bin/create.sql
#cp create.sql eXtremeDB/target/bin

start_time=$(date +%s.%N)
cd eXtremeDB/target/bin
./xsql -b -c xsql.cfg -p 5001 -f create.sql;

cd ../../..

end_time=$(date +%s.%N)
elapsed_time=$(echo "$end_time - $start_time" | bc)

compression=$(sh compression.sh  | tail -n 1)

echo "$dataset $compression ${elapsed_time}s" >> time_and_compression.txt

cat time_and_compression.txt

