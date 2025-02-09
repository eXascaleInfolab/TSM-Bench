#!/bin/sh
ps -ef | grep 'druid' | grep -v grep | awk '{print $2}' | xargs -r kill -9

echo " start Druid install"


pip3 install pydruid


#wget https://dlcdn.apache.org/druid/25.0.0/apache-druid-25.0.0-bin.tar.gz
wget https://archive.apache.org/dist/druid/25.0.0/apache-druid-25.0.0-bin.tar.gz


tar -xf apache-druid-25.0.0-bin.tar.gz
rm apache-druid-25.0.0-bin.tar.gz*

cp main.config apache-druid-25.0.0/conf/druid/single-server/medium/broker
#echo "start Druid server"

#time ./apache-druid-25.0.0/bin/start-single-server-medium &
