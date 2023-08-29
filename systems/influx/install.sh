#!/bin/sh

sudo systemctl stop influxd


pip3 install influxdb
>>>>>>> 8ff33e4e34f9d09531ea520d1ef987048386d8e9
wget https://dl.influxdata.com/influxdb/releases/influxdb-1.7.10_linux_amd64.tar.gz
tar xvfz influxdb-1.7.10_linux_amd64.tar.gz
rm influxdb-1.7.10_linux_amd64.tar.gz
sudo ./influxdb-1.7.10-1/usr/bin/influxd &
sleep 5
time sudo ./influxdb-1.7.10-1/usr/bin/influx -import -path=../../datasets/d1-influxdb.csv -precision=ms
sudo du -sh /var/lib/influxdb/data/d1

