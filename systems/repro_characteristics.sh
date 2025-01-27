#!/bin/bash

cd ../compression/

python3 generate_datasets.py

sleep 120

python3 generate_influx.py datasets

sleep 20

cd ../systems/clickhouse
sh load_compression.sh ../../compression/datasets

cd ../influx
sh load_compression.sh ../../compression/datasets_influx/

cd ../timescaledb
sh load_compression.sh ../../compression/datasets


