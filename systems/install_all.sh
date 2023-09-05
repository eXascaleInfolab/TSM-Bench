#!/bin/sh

# TO LOAD D2: 
# load.sh will load d1 to the systems, to load d2, uncomment the respective lines in the ./load.sh of each system


# ClickHouse
cd clickhouse
sh ./install.sh
sh ./launch.sh
cd ..

# Druid
#cd druid
#sh ./install.sh
#sh ./launch.sh
#cd ..

# ExtremeDB
cd extremedb
sh ./install.sh
cd ..

# Influx
# cd influx
# sh ./install.sh
# cd ..

# MonetDB
cd monetdb
sh ./install.sh
sh ./launch.sh
cd ..


# QuestDB
cd questdb
sh ./install.sh
sh ./launch.sh
cd ..

# TimescaleDB
cd  timescaledb
sh ./install.sh
cd ..


