#!/bin/sh

# ClickHouse
cd clickhouse
sh ./install.sh
cd ..

# Druid
cd druid
sh ./install.sh
cd ..

# ExtremeDB
cd extremedb
source ./install.sh
cd ..

# Influx
cd influx
sh ./install.sh
cd ..

# MonetDB
cd monetdb
sh ./install.sh
cd ..


# QuestDB
cd questdb
sh ./install.sh
cd ..

# TimescaleDB
cd  timescaledb
sh ./install.sh
cd ..
