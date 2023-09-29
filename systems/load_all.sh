#!/bin/sh

dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi
echo "loading $dataset"



# TimescaleDB
cd  timescaledb
sh ./load.sh $dataset
cd ..

# ClickHouse
cd clickhouse
sh ./load.sh $dataset
cd ..

# ExtremeDB
cd extremedb
sh ./load.sh $dataset
cd ..


# MonetDB
cd monetdb
sh ./load.sh $dataset
cd ..


# QuestDB
cd questdb
sh ./load.sh $dataset
cd ..

sh stop_all.sh


# TimescaleDB
cd  timescaledb
sh ./load.sh $dataset
cd ..


# Influx
cd influx
sh ./load.sh $dataset
cd ..

sh stop_all.sh

# Druid
cd druid
sh ./load.sh $dataset
cd ..
