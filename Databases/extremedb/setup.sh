#!/bin/bash

cd eXtremeDB/target/bin
./xsql -b -c xsql.cfg -p 5001 -f create.sql;

du -sh eXtremeDB/target/bin/datapoints.dbs
