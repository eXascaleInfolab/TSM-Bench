#!/bin/sh

sudo ./influxdb-1.7.10-1/usr/bin/influx -import -path=../../datasets/d1-influxdb.csv -precision=ms > /dev/null

sudo du -sh /var/lib/influxdb/data/d1



