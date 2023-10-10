#!/bin/sh

# Download the files with muted output
wget -O d2_1_4.csv https://zenodo.org/record/8393992/files/d2_aa?download=1 &
wget -O d2_2_4.csv https://zenodo.org/record/8394000/files/d2_ab?download=1 > /dev/null 2>&1 &
wget -O d2_3_4.csv https://zenodo.org/record/8394002/files/d2_ac?download=1 > /dev/null 2>&1 &
wget -O d2_4_4.csv https://zenodo.org/record/8394004/files/d2_ad?download=1 > /dev/null 2>&1 &

wait

# Concatenate the downloaded files
cat d2_1_4.csv d2_2_4.csv d2_3_4.csv d2_4_4.csv > d2.csv

# Remove individual files
rm d2_*
