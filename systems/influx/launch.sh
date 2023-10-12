#!/bin/sh

./influxdb-1.7.10-1/usr/bin/influxd 
sleep 10
echo "influx launched"

echo $!
