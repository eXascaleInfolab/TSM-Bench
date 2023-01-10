#!/bin/sh

wget https://github.com/questdb/questdb/releases/download/6.6.1/questdb-6.6.1-rt-linux-amd64.tar.gz

tar -xf questdb-6.6.1-rt-linux-amd64.tar.gz
rm questdb-6.6.1-rt-linux-amd64.tar.gz

#cp server.conf ../../../../.questdb/conf/
#sudo cp server.conf /root/.questdb/conf/

# sudo ./questdb.sh start
