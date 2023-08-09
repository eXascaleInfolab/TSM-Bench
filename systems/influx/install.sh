#!/bin/sh


wget https://dl.influxdata.com/influxdb/releases/influxdb-1.7.10_linux_amd64.tar.gz
tar xvfz influxdb-1.7.10_linux_amd64.tar.gz
rm influxdb-1.7.10_linux_amd64.tar.gz
time sudo ./influxdb-1.7.10-1/usr/bin/influx -import -path=../../datasets/d1-influxdb.csv -precision=ms
sudo du -sh /var/lib/influxdb/data/d1

