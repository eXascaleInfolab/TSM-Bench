#!/bin/sh

# ClickHouse
cd clickhouse
sh ./create.sh
cd ..

# Druid
cd druid
sh ./create.sh
cd ..

# ExtremeDB
cd extremedb
source ./create.sh
cd ..

# Influx
cd influx
sh ./create.sh
cd ..

# MonetDB
cd monetdb
sh ./create.sh
cd ..


# QuestDB
cd questdb
sh ./create.sh
cd ..

# TimescaleDB
cd  timescaledb
sh ./create.sh
cd ..
