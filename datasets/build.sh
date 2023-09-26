#!/bin/sh

dataset="d1"

if [ $# -ge 1 ]; then
    dataset="$1"
fi

if [ "$dataset" = "d1" ];then
	mkdir -p splits
	cat d1_splits/datasets_splits.* > datasets.tar.gz
	tar -zxvf datasets.tar.gz
	mv datasets/* ./
	rm datasets -r
	rm datasets.tar.gz

	python3 generate_influx.py d1
fi 


if [ "$dataset" = "d2" ];then
	mkdir d2
	cd d2

	wget https://zenodo.org/record/7701240/files/d2_p1.tar.gz
	wget https://zenodo.org/record/7701425/files/d2_p2.tar.gz

	tar -xf d2_p*.tar.gz
	rm d2_p*.tar.gz

	cat d1.csv d2.csv d3.csv > d2_full.csv
	rm  d2.csv d3.csv

	python3 generate_influx.py d2
fi

head -n 1 $dataset.csv > ${dataset}_tail.csv && tail -n 1 ${dataset}.csv >> ${datase}_tail.csv



