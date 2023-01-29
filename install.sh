#!/bin/sh

wget https://dl.influxdata.com/influxdb/releases/influxdb-1.7.10_linux_amd64.tar.gz
tar xvfz influxdb-1.7.10_linux_amd64.tar.gz
rm influxdb-1.7.10_linux_amd64.tar.gz

rm influxdb-1.7.10-1/etc/influxdb/influxdb.conf
cp influxdb.conf influxdb-1.7.10-1/etc/influxdb/

# sudo mkdir -p /etc/influxdb/ && sudo cp influxdb.conf /etc/influxdb/
export INFLUXDB_CONFIG_PATH=/etc/influxdb/influxdb.conf


time sudo ./influxdb-1.7.10-1/usr/bin/influx -import -path=../../Datasets/d1-influxdb.csv -precision=ms

sudo du -sh /var/lib/influxdb/data/d1

