#!/bin/sh

mkdir -p splits 
cat d1_splits/datasets_splits.* > datasets.tar.gz
tar -zxvf datasets.tar.gz
mv datasets/* ./
rm datasets -r
rm datasets.tar.gz

python3 generate_influx.py

 head -1 d1.csv > last_row_d1.csv && tail -1 d1.csv >> last_row_d1.csv
