#!/bin/sh


sudo killall --user influxdb
sudo killall --user telegraf
sudo kill -9 $(sudo lsof -t -i:8080)
ps -ef | grep 'influx' | grep -v grep | awk '{print $2}' | sudo xargs -r kill -9

