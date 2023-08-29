#!/bin/sh

sudo ./influxdb-1.7.10-1/usr/bin/influxd > /dev/null 2>&1 &

sleep 10
echo "influx launched"
