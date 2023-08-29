# ClickHouse
echo "############Clickhouse##########"
cd clickhouse
sh ./setup.sh
cd ..


# ExtremeDB
echo "############ExtremeDB##########"
cd extremedb
source ./setup.sh
cd ..

# Influx
echo "############Influx##########"
cd influx
sh ./setup.sh
cd ..

# MonetDB
echo "############MonetDB##########"
cd monetdb
sh ./setup.sh
cd ..


# QuestDB
echo "############QuestDB##########"
cd questdb
sh ./setup.sh
cd ..

# TimescaleDB
echo "############TimescaleDB##########"
cd  timescaledb
sh ./setup.sh
cd ..
# Druid
echo "############Druid##########"
cd druid
sh ./setup.sh
cd ..
