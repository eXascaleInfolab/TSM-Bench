#!/bin/sh

time ./apache-druid-25.0.0/bin/start-single-server-medium &
du -sh ./apache-druid-25.0.0/var/druid/segment-cache/d1
