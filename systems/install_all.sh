#!/bin/sh

# TO LOAD D2: 
# load.sh will load d1 to the systems, to load d2, uncomment the respective lines in the ./load.sh of each system


# ClickHouse
cd clickhouse
sh ./install.sh
sh ./launch.sh
sh ./load.sh
cd ..

# Druid
#cd druid
#sh ./install.sh
#sh ./launch.sh
#sh ./load.sh
#cd ..

# ExtremeDB
cd extremedb
sh ./install.sh
sh ./load.sh
cd ..

# Influx
# cd influx
# sh ./install.sh
# sh ./launch.sh
# sh ./load.sh
# cd ..

# MonetDB
cd monetdb
sh ./install.sh
sh ./launch.sh
sh ./load.sh
cd ..


# QuestDB
cd questdb
sh ./install.sh
sh ./launch.sh
sh ./load.sh
cd ..

# TimescaleDB
cd  timescaledb
sh ./install.sh
sh ./load.sh
cd ..


