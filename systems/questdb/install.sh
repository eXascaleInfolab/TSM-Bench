#!/bin/sh

sudo kill -9 `sudo lsof -t -i:9000`
sleep 2

wget https://github.com/questdb/questdb/releases/download/6.4.1/questdb-6.4.1-rt-linux-amd64.tar.gz

tar -xf questdb-6.4.1-rt-linux-amd64.tar.gz
rm questdb-6.4.1-rt-linux-amd64.tar.gz

sudo mkdir /root/.questdb/conf
sudo mkdir $HOME/.questdb/conf/
sudo cp server.conf $HOME/.questdb/conf/
sudo cp server.conf /root/.questdb/conf/

sudo ./questdb-6.4.1-rt-linux-amd64/bin/questdb.sh start

sudo cp server.conf $HOME/.questdb/conf/
sudo cp server.conf /root/.questdb/conf/

sleep 25

