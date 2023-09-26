#!/bin/sh

dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi
echo "loading $dataset"


# ClickHouse
cd clickhouse
sh ./load.sh $dataset
cd ..

# Druid
cd druid
sh ./load.sh $dataset
cd ..

# ExtremeDB
cd extremedb
source ./load.sh $dataset
cd ..


# MonetDB
cd monetdb
sh ./load.sh $dataset
cd ..


# QuestDB
cd questdb
sh ./load.sh $dataset
cd ..

# TimescaleDB
cd  timescaledb
sh ./load.sh $dataset
cd ..


# Influx
cd influx
sh ./load.sh $dataset
cd ..
