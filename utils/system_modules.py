from systems import  influx ,extremedb, timescaledb , questdb  , monetdb , clickhouse , druid


system_module_map = { "influx" : influx,
    "extremedb" : extremedb,
    "clickhouse" : clickhouse,
    "questdb" : questdb,
    "monetdb" : monetdb,
    "druid" : druid,
    "timescaledb" : timescaledb
}