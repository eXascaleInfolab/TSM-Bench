#!/bin/sh

sudo pip3 install clickhouse-driver

sudo docker pull clickhouse/clickhouse-server

sudo kill -9 $(lsof -t -i:9000)

sudo docker run -d --name clickhouse-container \
	-p 8123:8123 -p 9000:9000 \
	clickhouse/clickhouse-server


sudo docker start clickhouse-container

sudo docker exec -it clickhouse-container clickhouse-client --query "CREATE TABLE IF NOT EXISTS d1 (  \
	time DateTime64(9) CODEC(Gorilla), id_station String, s0 Float32 , s1 Float32 , s2 Float32 , s3 Float32 , s4 Float32 , s5 Float32 , s6 Float32 , s7 Float32 , s8 Float32 , s9 Float32 , s10 Float32 , s11 Float32 , s12 Float32 , s13 Float32 , s14 Float32 , s15 Float32 , s16 Float32 , s17 Float32 , s18 Float32 , s19 Float32 , s20 Float32 , s21 Float32 , s22 Float32 , s23 Float32 , s24 Float32 , s25 Float32 , s26 Float32 , s27 Float32 , s28 Float32 , s29 Float32 , s30 Float32 , s31 Float32 , s32 Float32 , s33 Float32 , s34 Float32 , s35 Float32 , s36 Float32 , s37 Float32 , s38 Float32 , s39 Float32 , s40 Float32 , s41 Float32 , s42 Float32 , s43 Float32 , s44 Float32 , s45 Float32 , s46 Float32 , s47 Float32 , s48 Float32 , s49 Float32 , s50 Float32 , s51 Float32 , s52 Float32 , s53 Float32 , s54 Float32 , s55 Float32 , s56 Float32 , s57 Float32 , s58 Float32 , s59 Float32 , s60 Float32 , s61 Float32 , s62 Float32 , s63 Float32 , s64 Float32 , s65 Float32 , s66 Float32 , s67 Float32 , s68 Float32 , s69 Float32 , s70 Float32 , s71 Float32 , s72 Float32 , s73 Float32 , s74 Float32 , s75 Float32 , s76 Float32 , s77 Float32 , s78 Float32 , s79 Float32 , s80 Float32 , s81 Float32 , s82 Float32 , s83 Float32 , s84 Float32 , s85 Float32 , s86 Float32 , s87 Float32 , s88 Float32 , s89 Float32 , s90 Float32 , s91 Float32 , s92 Float32 , s93 Float32 , s94 Float32 , s95 Float32 , s96 Float32 , s97 Float32 , s98 Float32 , s99 Float32 \
	) ENGINE = MergeTree() PARTITION BY toYYYYMMDD(time) ORDER BY (id_station, time) Primary key (id_station, time);" 


# loading 
# time ( cat '../../Datasets/d1.csv' | sudo docker exec -i clickhouse-container clickhouse-client --format_csv_delimiter="," --query="INSERT INTO d1 FORMAT CSVWithNames" ) 

cat '../../datasets/d1.csv' | sudo docker exec -i clickhouse-container clickhouse-client --format_csv_delimiter="," --query="INSERT INTO d1 FORMAT CSVWithNames" 



# compression
sudo docker exec -it clickhouse-container clickhouse-client --query "SELECT table,
				formatReadableSize(sum(bytes)) as size
				FROM system.parts
				WHERE active AND table='d1'
				GROUP BY table;"


sudo docker stop clickhouse-container

# sudo docker cp config.xml clickhouse-container:/etc/clickhouse-server/

