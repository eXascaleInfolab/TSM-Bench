#!/bin/sh

#mkdir -p splits 
#cat d1_splits/datasets_splits.* > datasets.tar.gz
#tar -zxvf datasets.tar.gz
#mv datasets/* ./
#rm datasets -r
#rm datasets.tar.gz

wget -O d1.csv https://zenodo.org/record/8385578/files/d1.csv?download=1

python3 generate_influx.py



# head -n 1 d1.csv > d1_tail.csv && tail -n 1 d1.csv >> d1_tail.csv
