#!/bin/bash

# THE FOLLOWING SCRIPT WILL SETUP AND LOAD D1, TO LOAD D2 UNCOMMENT THE LINES BELOW 


cd eXtremeDB/target/bin
./xsql -b -c xsql.cfg -p 5001 -f create.sql;

du -sh datapoints.dbs


#./xsql -b -c xsql.cfg -p 5001 -f create2.sql;
#du -sh datapoints.dbs
