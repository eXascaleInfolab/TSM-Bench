#!/bin/sh

dataset="d1"

if [ $# -ge 1 ]; then
    dataset="$1"
fi

if [ "$dataset" = "d1" ];then
	#mkdir -p splits
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
	wget -O d2_1_4.csv https://zenodo.org/record/8393992/files/d2_aa?download=1
	wget -O d2_2_4.csv https://zenodo.org/record/8394000/files/d2_ab?download=1
	wget -O d2_3_4.csv https://zenodo.org/record/8394002/files/d2_ac?download=1
	wget -O d2_4_4.csv https://zenodo.org/record/8394004/files/d2_ad?download=1
	
	(head -n -1 d2_1_4.csv; head -n -1 d2_2_4.csv; head -n -1 d2_3_4.csv; head -n -1 d2_4_4.csv) > d2.csv
	
	rm d2_*

	python3 generate_influx.py d2
fi

head -n 1 $dataset.csv > ${dataset}_tail.csv && tail -n 1 ${dataset}.csv >> ${dataset}_tail.csv



