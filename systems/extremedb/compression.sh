#!/bin/sh

# THE FOLLOWING SCRIPT WILL PRINT STORAGE SIZE FOR D1, TO SHOW D2 UNCOMMENT THE LINES BELOW 

cd eXtremeDB/target/bin
./xsql -b -c xsql.cfg -p 5001 -f create.sql;

du -sh datapoints.dbs
#du -sh datapoints2.dbs
