#!/bin/sh


# ClickHouse
cd clickhouse
sh ./launch.sh
cd ..

# Druid
cd druid
sh ./launch.sh
cd ..

# ExtremeDB
cd extremedb
sh ./launch.sh
cd ..

# Influx
cd influx
sh ./launch.sh
cd ..

# MonetDB
cd monetdb
sh ./launch.sh
cd ..


# QuestDB
cd questdb
sh ./launch.sh
cd ..

# TimescaleDB
cd  timescaledb
sh ./launch.sh
cd ..