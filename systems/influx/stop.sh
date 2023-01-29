#!/bin/sh


ps -ef | grep 'influx' | grep -v grep | awk '{print $2}' | sudo xargs -r kill -9

