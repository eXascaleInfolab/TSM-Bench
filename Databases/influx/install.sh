#!/bin/sh

wget https://dl.influxdata.com/influxdb/releases/influxdb-1.7.10_linux_amd64.tar.gz
tar xvfz influxdb-1.7.10_linux_amd64.tar.gz
rm influxdb-1.7.10_linux_amd64.tar.gz

rm influxdb-1.7.10-1/etc/influxdb/influxdb.conf
cp influxdb.conf influxdb-1.7.10-1/etc/influxdb/

# sudo mkdir -p /etc/influxdb/ && sudo cp influxdb.conf /etc/influxdb/
export INFLUXDB_CONFIG_PATH=/etc/influxdb/influxdb.conf
