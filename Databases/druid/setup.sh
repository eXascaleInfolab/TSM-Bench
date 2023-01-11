#!/bin/sh

current=$(pwd)

sed 's?path_to_file?'`pwd`/../../Datasets/d1.csv'?' load_template.json > load.json

time ./apache-druid-25.0.0/bin/post-index-task --file load.json --url http://localhost:8081 &

du -sh ./apache-druid-25.0.0/var/druid/segment-cache/d1
