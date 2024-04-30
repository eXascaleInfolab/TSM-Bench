#!/bin/sh
cd systems
was_in_root=$?

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
sh ./install.sh
cd ..

#Influx
cd influx
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


# TimescaleDB
cd  timescaledb
sh ./install.sh
cd ..





if [ $was_in_root -eq 0 ]; then
    cd ..
fi
