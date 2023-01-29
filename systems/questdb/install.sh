#!/bin/sh

wget https://github.com/questdb/questdb/releases/download/6.4.1/questdb-6.4.1-rt-linux-amd64.tar.gz

tar -xf questdb-6.4.1-rt-linux-amd64.tar.gz
rm questdb-6.4.1-rt-linux-amd64.tar.gz

sudo cp server.conf $HOME/.questdb/conf/
#sudo cp server.conf /root/.questdb/conf/

# sudo ./questdb.sh start
