#!/bin/sh


time sudo ./influxdb-1.7.10-1/usr/bin/influx -import -path=../../Datasets/d1-influxdb.csv -precision=ms

sudo du -sh /var/lib/influxdb/data/d1



