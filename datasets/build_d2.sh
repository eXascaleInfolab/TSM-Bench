#!/bin/sh

mkdir d2
cd d2

wget https://zenodo.org/record/7701240/files/d2_p1.tar.gz
wget https://zenodo.org/record/7701425/files/d2_p2.tar.gz

tar -xf d2_p*.tar.gz
rm d2_p*.tar.gz

cat d1.csv d2.csv d3.csv > d2_full.csv
rm d1.csv d2.csv d3.csv 

tail -1 d2.csv > last_row_d2.csv
