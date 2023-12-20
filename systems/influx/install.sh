#!/bin/sh

sudo killall --user influxdb
sudo killall --user telegraf
sudo kill -9 $(sudo lsof -t -i:8080)
ps -ef | grep 'influx' | grep -v grep | awk '{print $2}' | sudo xargs -r kill -9

sleep 10

sudo systemctl stop influxd

pip3 install influxdb

sudo apt install influxdb


wget https://dl.influxdata.com/influxdb/releases/influxdb-1.7.10_linux_amd64.tar.gz
tar xvfz influxdb-1.7.10_linux_amd64.tar.gz
rm influxdb-1.7.10_linux_amd64.tar.gz
#sudo ./influxdb-1.7.10-1/usr/bin/influxd &
cp influxdb.conf influxdb-1.7.10-1/etc/influxdb/influxdb.conf 

sudo chmod -R 777 /var/lib/influxdb

