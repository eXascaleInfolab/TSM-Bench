#!/bin/sh

sleep 25 

dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi
echo "loading $dataset"


container_name="timescaledb-container"
docker start "$container_name"
#sudo docker exec -it timescaledb-container psql -U postgres

# Wait for the container to be in a running state
while true; do
    container_status=$(docker inspect -f '{{.State.Status}}' "$container_name")
    echo "$container_status"
    if [ "$container_status" = "running" ]; then
        break
    fi
    sleep 1
done

sleep 5

docker exec -it timescaledb-container psql -U postgres -c  "DROP TABLE IF EXISTS $dataset CASCADE;"


sleep 5

start_time=$(date +%s.%N)
docker exec -it timescaledb-container psql -U postgres -c  "CREATE TABLE $dataset ( time TIMESTAMP NOT NULL, id_station TEXT NOT NULL, s0 DOUBLE PRECISION , s1 DOUBLE PRECISION , s2 DOUBLE PRECISION , s3 DOUBLE PRECISION , s4 DOUBLE PRECISION , s5 DOUBLE PRECISION , s6 DOUBLE PRECISION , s7 DOUBLE PRECISION , s8 DOUBLE PRECISION , s9 DOUBLE PRECISION , s10 DOUBLE PRECISION , s11 DOUBLE PRECISION , s12 DOUBLE PRECISION , s13 DOUBLE PRECISION , s14 DOUBLE PRECISION , s15 DOUBLE PRECISION , s16 DOUBLE PRECISION , s17 DOUBLE PRECISION , s18 DOUBLE PRECISION , s19 DOUBLE PRECISION , s20 DOUBLE PRECISION , s21 DOUBLE PRECISION , s22 DOUBLE PRECISION , s23 DOUBLE PRECISION , s24 DOUBLE PRECISION , s25 DOUBLE PRECISION , s26 DOUBLE PRECISION , s27 DOUBLE PRECISION , s28 DOUBLE PRECISION , s29 DOUBLE PRECISION , s30 DOUBLE PRECISION , s31 DOUBLE PRECISION , s32 DOUBLE PRECISION , s33 DOUBLE PRECISION , s34 DOUBLE PRECISION , s35 DOUBLE PRECISION , s36 DOUBLE PRECISION , s37 DOUBLE PRECISION , s38 DOUBLE PRECISION , s39 DOUBLE PRECISION , s40 DOUBLE PRECISION , s41 DOUBLE PRECISION , s42 DOUBLE PRECISION , s43 DOUBLE PRECISION , s44 DOUBLE PRECISION , s45 DOUBLE PRECISION , s46 DOUBLE PRECISION , s47 DOUBLE PRECISION , s48 DOUBLE PRECISION , s49 DOUBLE PRECISION , s50 DOUBLE PRECISION , s51 DOUBLE PRECISION , s52 DOUBLE PRECISION , s53 DOUBLE PRECISION , s54 DOUBLE PRECISION , s55 DOUBLE PRECISION , s56 DOUBLE PRECISION , s57 DOUBLE PRECISION , s58 DOUBLE PRECISION , s59 DOUBLE PRECISION , s60 DOUBLE PRECISION , s61 DOUBLE PRECISION , s62 DOUBLE PRECISION , s63 DOUBLE PRECISION , s64 DOUBLE PRECISION , s65 DOUBLE PRECISION , s66 DOUBLE PRECISION , s67 DOUBLE PRECISION , s68 DOUBLE PRECISION , s69 DOUBLE PRECISION , s70 DOUBLE PRECISION , s71 DOUBLE PRECISION , s72 DOUBLE PRECISION , s73 DOUBLE PRECISION , s74 DOUBLE PRECISION , s75 DOUBLE PRECISION , s76 DOUBLE PRECISION , s77 DOUBLE PRECISION , s78 DOUBLE PRECISION , s79 DOUBLE PRECISION , s80 DOUBLE PRECISION , s81 DOUBLE PRECISION , s82 DOUBLE PRECISION , s83 DOUBLE PRECISION , s84 DOUBLE PRECISION , s85 DOUBLE PRECISION , s86 DOUBLE PRECISION , s87 DOUBLE PRECISION , s88 DOUBLE PRECISION , s89 DOUBLE PRECISION , s90 DOUBLE PRECISION , s91 DOUBLE PRECISION , s92 DOUBLE PRECISION , s93 DOUBLE PRECISION , s94 DOUBLE PRECISION , s95 DOUBLE PRECISION , s96 DOUBLE PRECISION , s97 DOUBLE PRECISION , s98 DOUBLE PRECISION , s99 DOUBLE PRECISION );"

sleep 10

docker exec -it timescaledb-container psql -U postgres -c  "SELECT create_hypertable('$dataset', 'time', chunk_time_interval=>'7 days'::INTERVAL);"


current="$(pwd)"

sleep 10
docker exec -it timescaledb-container psql -U postgres -c "COPY $dataset FROM '/var/lib/postgresql/data/TSM-Bench/datasets/$dataset.csv' DELIMITER ',' CSV HEADER;";

sleep 10
docker exec -it timescaledb-container psql -U postgres -c "ALTER TABLE $dataset SET (timescaledb.compress, timescaledb.compress_segmentby='id_station');
SELECT compress_chunk(i) FROM show_chunks('$dataset') i ORDER BY i DESC OFFSET 1;"


end_time=$(date +%s.%N)
elapsed_time=$(echo "$end_time - $start_time" | bc)

echo "computing compression"
compression="$(sh compression.sh $dataset | tail -n 1)"

echo "$dataset $compression ${elapsed_time}s"

echo "$dataset $compression ${elapsed_time}s" >> time_and_compression.txt

