#!/bin/sh

mkdir -p splits 
cat splits/datasets_splits.* > datasets.tar.gz
tar -zxvf datasets.tar.gz
mv datasets/* ./
rm datasets -r
rm datasets.tar.gz

python3 generate_influx.py
