#!/bin/sh


wget -O d2_1_4.csv https://zenodo.org/record/8393992/files/d2_aa?download=1
wget -O d2_2_4.csv https://zenodo.org/record/8394000/files/d2_ab?download=1
wget -O d2_3_4.csv https://zenodo.org/record/8394002/files/d2_ac?download=1
wget -O d2_4_4.csv https://zenodo.org/record/8394004/files/d2_ad?download=1

cat d2_1_4.csv d2_2_4.csv d2_3_4.csv d2_4_4.csv > d2.csv

rm d2_*

