#!/bin/sh

mkdir d2_splits
cd d2_splits 

wget https://zenodo.org/record/7591120/files/D2_part1.zip
wget https://zenodo.org/record/7586294/files/D2_part2.zip

unzip D2_part1.zip
unzip D2_part2.zip

rm D2_part*

cat datasets_splits.* > d2.tar.gz
tar -zxvf d2.tar.gz
mv d2/* ./
rm -r d2 
rm d2.tar.gz
mv d2.txt ../
cd ..
rm -r d2
