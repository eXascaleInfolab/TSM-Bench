#!/bin/sh

# sudo kill -9 `sudo lsof -t -i:5001`
cd eXtremeDB/target/bin
./xsql -i -c xsql.cfg -p 5001 
