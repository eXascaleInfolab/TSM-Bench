#!/bin/bash

cd ../compression/

python generate_datasets.py

sleep 120

# python generate_influx.py datasets

sleep 20

cd ../systems/clickhouse 
sh load_compression.sh ../../compression/datasets

cd ../timescaledb
sh load_compression.sh ../../compression/datasets
