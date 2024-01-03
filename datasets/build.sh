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
fi 


if [ "$dataset" = "d2" ];then
	wget -O d2_1_4.csv https://zenodo.org/record/8393992/files/d2_aa?download=1
  wget -O d2_2_4.csv https://zenodo.org/record/8394000/files/d2_ab?download=1
  wget -O d2_3_4.csv https://zenodo.org/record/8394002/files/d2_ac?download=1
  wget -O d2_4_4.csv https://zenodo.org/record/8394004/files/d2_ad?download=1

  header="time,id_station,s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20,s21,s22,s23,s24,s25,s26,s27,s28,s29,s30,s31,s32,s33,s34,s35,s36,s37,s38,s39,s40,s41,s42,s43,s44,s45,s46,s47,s48,s49,s50,s51,s52,s53,s54,s55,s56,s57,s58,s59,s60,s61,s62,s63,s64,s65,s66,s67,s68,s69,s70,s71,s72,s73,s74,s75,s76,s77,s78,s79,s80,s81,s82,s83,s84,s85,s86,s87,s88,s89,s90,s91,s92,s93,s94,s95,s96,s97,s98,s99"

  echo "$header" > d2.csv
  sed '1d;$d' d2_1_4.csv >> d2.csv
  sed '1d;$d' d2_2_4.csv >> d2.csv
  sed '1d;$d' d2_3_4.csv >> d2.csv
  sed '1d;$d' d2_4_4.csv >> d2.csv
fi

