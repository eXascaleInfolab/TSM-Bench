#!/bin/sh

du -sh ./apache-druid-25.0.0/var/druid/segment-cache/d1

cd eXtremeDB/target/bin
./xsql -b -c xsql.cfg -p 5001 -f create.sql;

du -sh datapoints.dbs