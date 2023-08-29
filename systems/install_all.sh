#!/bin/sh

# ClickHouse
cd clickhouse
sh ./install.sh
sh ./launch.sh
sh ./setup.sh
cd ..

# Druid
cd druid
sh ./install.sh
sh ./launch.sh
sh ./setup.sh
cd ..

# ExtremeDB
cd extremedb
sh ./install.sh
sh ./launch.sh
sh ./setup.sh
cd ..

# Influx
# cd influx
# sh ./install.sh
# sh ./launch.sh
# sh ./setup.sh
# cd ..

# MonetDB
cd monetdb
sh ./install.sh
sh ./launch.sh
sh ./setup.sh
cd ..


# QuestDB
cd questdb
sh ./install.sh
sh ./launch.sh
sh ./setup.sh
cd ..

# TimescaleDB
cd  timescaledb
sh ./install.sh
sh ./launch.sh
sh ./setup.sh
cd ..


