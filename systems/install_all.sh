#!/bin/sh


# ClickHouse
cd clickhouse
sh ./install.sh
cd ..

# Druid
cd druid
sh ./install.sh
sh ./launch.sh
cd ..

# ExtremeDB
cd extremedb
sh ./install.sh
cd ..

# MonetDB
cd monetdb
sh ./install.sh
cd ..


# QuestDB
cd questdb
sh install.sh
cd ..

cd extremedb
sh ./install.sh
cd ..

cd questdb
sh install.sh
cd ..

# TimescaleDB
cd  timescaledb
sh ./install.sh
cd ..

#Influx
cd influx
sh ./install.sh
cd ..

