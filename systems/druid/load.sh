#!/bin/sh

# THE FOLLOWING SCRIPT WILL SETUP AND LOAD D1, TO LOAD D2 UNCOMMENT THE LINES BELOW 


current=$(pwd)


echo "start!" 
sed 's?path_to_file?'`pwd`/../../datasets/d1.csv'?' load_template.json > load.json
echo "load json"
time ./apache-druid-25.0.0/bin/post-index-task --file load.json --url http://localhost:8081 &


echo "load database"
du -sh ./apache-druid-25.0.0/var/druid/segment-cache/d1

echo "DONE"


#sed 's?path_to_file?'`pwd`/../../datasets/d2.csv'?' load_template.json > load.json
#echo "load json"
#time ./apache-druid-25.0.0/bin/post-index-task --file load.json --url http://localhost:8081 &
