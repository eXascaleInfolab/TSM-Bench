#!/bin/sh

dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi
echo "loading $dataset"

cd ../systems

sh stop_all.sh


# TimescaleDB
echo "loading data into TimescaleDB"
cd  timescaledb
sh ./load.sh $dataset
cd ..

echo "loading data into Clickhouse"
# ClickHouse
cd clickhouse
sh ./load.sh $dataset
cd ..

echo "loading data into ExtremeDB"
# ExtremeDB
cd extremedb
sh ./load.sh $dataset
cd ..

echo "loading data into MonetDB"
# MonetDB
cd monetdb
sh ./load.sh $dataset
cd ..

echo "loading data into QuestDB"
# QuestDB
cd questdb
sh ./load.sh $dataset
cd ..

sh stop_all.sh


# TimescaleDB
echo "loading data into TimescaleDB"
cd  timescaledb
sh ./load.sh $dataset
cd ..

echo "loading data into Influx"
# Influx
cd influx
sh ./load.sh $dataset
cd ..

sh stop_all.sh

echo "loading data into Druid"
# Druid
cd druid
sh ./load.sh $dataset
cd ..
