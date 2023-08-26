#!/bin/sh

# ClickHouse
cd clickhouse
sh ./setup.sh
cd ..

# Druid
cd druid
sh ./setup.sh
cd ..

# ExtremeDB
cd extremedb
source ./setup.sh
cd ..

# Influx
cd influx
sh ./setup.sh
cd ..

# MonetDB
cd monetdb
sh ./setup.sh
cd ..


# QuestDB
cd questdb
sh ./setup.sh
cd ..

# TimescaleDB
cd  timescaledb
sh ./setup.sh
cd ..
