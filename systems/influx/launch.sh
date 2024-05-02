#!/bin/sh


log_file="influxdb.log"

# "" > "$log_file"

sudo ./influxdb-1.7.10-1/usr/bin/influxd > "$log_file" 2>&1 &

sleep 10
echo "influx launched"

