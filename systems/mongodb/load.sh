#!/bin/sh

# Load a commaseperated file into a mongodb database and measure the time it takes to load it

sudo docker start mongo 
sleep 10
# THE FOLLOWING SCRIPT WILL SETUP AND LOAD D1, TO LOAD D2 UNCOMMENT THE LINES BELOW 

dataset="d1"

current="$(pwd)"


# we need the file without header to specify the types

if [ -f "../../datasets/${dataset}_no_header.csv" ]; then
    echo "headerless file exists."
else
  sed '1d' ../../datasets/$dataset.csv > ../../datasets/${dataset}_no_header.csv
fi

start_time=$(date +%s.%N)

sudo docker cp ../../datasets/${dataset}_no_header.csv mongo:/tmp/$dataset.csv

## import the data
docker exec -it mongo mongoimport -d $dataset -c $dataset --type csv --file /tmp/$dataset.csv  --columnsHaveTypes \
    -f "time.date(2006-01-02T15:04:05),id_station.string(),s0.double(),s1.double(),s2.double(),s3.double(),s4.double(),s5.double(),s6.double(),s7.double(),s8.double(),s9.double(),s10.double(),s11.double(),s12.double(),s13.double(),s14.double(),s15.double(),s16.double(),s17.double(),s18.double(),s19.double(),s20.double(),s21.double(),s22.double(),s23.double(),s24.double(),s25.double(),s26.double(),s27.double(),s28.double(),s29.double(),s30.double(),s31.double(),s32.double(),s33.double(),s34.double(),s35.double(),s36.double(),s37.double(),s38.double(),s39.double(),s40.double(),s41.double(),s42.double(),s43.double(),s44.double(),s45.double(),s46.double(),s47.double(),s48.double(),s49.double(),s50.double(),s51.double(),s52.double(),s53.double(),s54.double(),s55.double(),s56.double(),s57.double(),s58.double(),s59.double(),s60.double(),s61.double(),s62.double(),s63.double(),s64.double(),s65.double(),s66.double(),s67.double(),s68.double(),s69.double(),s70.double(),s71.double(),s72.double(),s73.double(),s74.double(),s75.double(),s76.double(),s77.double(),s78.double(),s79.double(),s80.double(),s81.double(),s82.double(),s83.double(),s84.double(),s85.double(),s86.double(),s87.double(),s88.double(),s89.double(),s90.double(),s91.double(),s92.double(),s93.double(),s94.double(),s95.double(),s96.double(),s97.double(),s98.double(),s99.double()"


end_time=$(date +%s.%N)
elapsed_time=$(echo "$end_time - $start_time" | bc)
echo "Loading time: $elapsed_time seconds" > loading_time_$dataset.txt


echo "comression"
sh compression.sh


## uncoment the following for D2 ##
###################################
# echo "start loading!"
#mclient -p54320 -d mydb --interactive --timer=performance -s "DROP TABLE IF EXISTS d2; \
#	CREATE TABLE d2 ( time TIMESTAMP NOT NULL, id_station STRING, s0 DOUBLE PRECISION , s1 DOUBLE PRECISION , s2 DOUBLE PRECISION , s3 DOUBLE PRECISION , s4 DOUBLE PRECISION , s5 DOUBLE PRECISION , s6 DOUBLE PRECISION , s7 DOUBLE PRECISION , s8 DOUBLE PRECISION , s9 DOUBLE PRECISION , s10 DOUBLE PRECISION , s11 DOUBLE PRECISION , s12 DOUBLE PRECISION , s13 DOUBLE PRECISION , s14 DOUBLE PRECISION , s15 DOUBLE PRECISION , s16 DOUBLE PRECISION , s17 DOUBLE PRECISION , s18 DOUBLE PRECISION , s19 DOUBLE PRECISION , s20 DOUBLE PRECISION , s21 DOUBLE PRECISION , s22 DOUBLE PRECISION , s23 DOUBLE PRECISION , s24 DOUBLE PRECISION , s25 DOUBLE PRECISION , s26 DOUBLE PRECISION , s27 DOUBLE PRECISION , s28 DOUBLE PRECISION , s29 DOUBLE PRECISION , s30 DOUBLE PRECISION , s31 DOUBLE PRECISION , s32 DOUBLE PRECISION , s33 DOUBLE PRECISION , s34 DOUBLE PRECISION , s35 DOUBLE PRECISION , s36 DOUBLE PRECISION , s37 DOUBLE PRECISION , s38 DOUBLE PRECISION , s39 DOUBLE PRECISION , s40 DOUBLE PRECISION , s41 DOUBLE PRECISION , s42 DOUBLE PRECISION , s43 DOUBLE PRECISION , s44 DOUBLE PRECISION , s45 DOUBLE PRECISION , s46 DOUBLE PRECISION , s47 DOUBLE PRECISION , s48 DOUBLE PRECISION , s49 DOUBLE PRECISION , s50 DOUBLE PRECISION , s51 DOUBLE PRECISION , s52 DOUBLE PRECISION , s53 DOUBLE PRECISION , s54 DOUBLE PRECISION , s55 DOUBLE PRECISION , s56 DOUBLE PRECISION , s57 DOUBLE PRECISION , s58 DOUBLE PRECISION , s59 DOUBLE PRECISION , s60 DOUBLE PRECISION , s61 DOUBLE PRECISION , s62 DOUBLE PRECISION , s63 DOUBLE PRECISION , s64 DOUBLE PRECISION , s65 DOUBLE PRECISION , s66 DOUBLE PRECISION , s67 DOUBLE PRECISION , s68 DOUBLE PRECISION , s69 DOUBLE PRECISION , s70 DOUBLE PRECISION , s71 DOUBLE PRECISION , s72 DOUBLE PRECISION , s73 DOUBLE PRECISION , s74 DOUBLE PRECISION , s75 DOUBLE PRECISION , s76 DOUBLE PRECISION , s77 DOUBLE PRECISION , s78 DOUBLE PRECISION , s79 DOUBLE PRECISION , s80 DOUBLE PRECISION , s81 DOUBLE PRECISION , s82 DOUBLE PRECISION , s83 DOUBLE PRECISION , s84 DOUBLE PRECISION , s85 DOUBLE PRECISION , s86 DOUBLE PRECISION , s87 DOUBLE PRECISION , s88 DOUBLE PRECISION , s89 DOUBLE PRECISION , s90 DOUBLE PRECISION , s91 DOUBLE PRECISION , s92 DOUBLE PRECISION , s93 DOUBLE PRECISION , s94 DOUBLE PRECISION , s95 DOUBLE PRECISION , s96 DOUBLE PRECISION , s97 DOUBLE PRECISION , s98 DOUBLE PRECISION , s99 DOUBLE PRECISION );  
#	COPY OFFSET 2 INTO d2 FROM '$current/../../datasets/d2.csv' USING DELIMITERS ',','\n'; 
#	select sum(columnsize)/1024/1024/1024 from storage where table='d2'; "


