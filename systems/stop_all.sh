#!/bin/sh


# ClickHouse
cd clickhouse
sh stop.sh
cd ..

# Druid
cd druid
sh stop.sh
cd ..

# ExtremeDB
cd extremedb
sh stop.sh
cd ..

# Influx
cd influx
sh stop.sh
cd ..

# MonetDB
cd monetdb
sh  stop.sh
cd ..


# QuestDB
cd questdb
sh stop.sh
cd ..

# TimescaleDB
cd  timescaledb
sh stop.sh
cd ..

