#!/bin/sh

# ClickHouse
cd clickhouse
sh ./load.sh
cd ..

# Druid
cd druid
sh ./load.sh
cd ..

# ExtremeDB
cd extremedb
source ./load.sh
cd ..

# Influx
cd influx
sh ./load.sh
cd ..

# MonetDB
cd monetdb
sh ./load.sh
cd ..


# QuestDB
cd questdb
sh ./load.sh
cd ..

# TimescaleDB
cd  timescaledb
sh ./load.sh
cd ..
