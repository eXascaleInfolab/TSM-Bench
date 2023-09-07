#!/bin/sh

sudo killall --user influxdb
sudo killall --user telegraf
sudo kill -9 $(sudo lsof -t -i:8080)
	sudo kill -9 $(sudo lsof -t -i:8080)
ps -ef | grep 'influx' | grep -v grep | awk '{print $2}' | sudo xargs -r kill -9

sleep 10

sudo systemctl stop influxd

pip3 install influxdb

sudo apt install influxdb


wget https://dl.influxdata.com/influxdb/releases/influxdb-1.7.10_linux_amd64.tar.gz
tar xvfz influxdb-1.7.10_linux_amd64.tar.gz
rm influxdb-1.7.10_linux_amd64.tar.gz
sudo ./influxdb-1.7.10-1/usr/bin/influxd &
sleep 15
#time sudo ./influxdb-1.7.10-1/usr/bin/influx -import -path=../../datasets/d1-influxdb.csv -precision=ms &
#sudo du -sh /var/lib/influxdb/data/d1
sh load.sh


