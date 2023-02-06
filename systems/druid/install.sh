#!/bin/sh

pip3 install pydruid


wget https://dlcdn.apache.org/druid/25.0.0/apache-druid-25.0.0-bin.tar.gz
tar -xf apache-druid-25.0.0-bin.tar.gz
rm apache-druid-25.0.0-bin.tar.gz

time ./apache-druid-25.0.0/bin/start-single-server-medium &


current=$(pwd)

sed 's?path_to_file?'`pwd`/../../datasets/d1.csv'?' load_template.json > load.json

time ./apache-druid-25.0.0/bin/post-index-task --file load.json --url http://localhost:8081 &

du -sh ./apache-druid-25.0.0/var/druid/segment-cache/d1


ps -ef | grep 'druid' | grep -v grep | awk '{print $2}' | xargs -r kill -9
