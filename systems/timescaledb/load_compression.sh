#!/bin/sh

# THE FOLLOWING SCRIPT WILL SETUP, LOAD, AND COMPUTE COMPRESSION FOR DATASETS FROM A GIVEN FOLDER IN TimescaleDB

# Check if a folder path is provided as an argument
if [ $# -ge 1 ]; then
    folder_path="$1"
else
    echo "No folder path provided."
    exit 1
fi

# Container name for TimescaleDB
container_name="timescaledb-container"

# Function to restart TimescaleDB container
restart_timescaledb() {
    # Stop TimescaleDB container if it is running
    docker stop "$container_name"
    sleep 5

    # Start TimescaleDB container
    docker start "$container_name"
    sleep 10
}

# Function to load a CSV file into TimescaleDB
load_dataset() {
    file_path="$1"
    dataset=$(basename "$file_path" .csv)
    
    # Drop existing table if it exists
    docker exec -it timescaledb-container psql -U postgres -c "DROP TABLE IF EXISTS $dataset CASCADE;"
    sleep 5

    # Create the table in TimescaleDB
    docker exec -it timescaledb-container psql -U postgres -c "CREATE TABLE $dataset (
        time TIMESTAMP NOT NULL,
        id_station TEXT NOT NULL,
        s0 DOUBLE PRECISION, s1 DOUBLE PRECISION, s2 DOUBLE PRECISION, s3 DOUBLE PRECISION, s4 DOUBLE PRECISION,
        s5 DOUBLE PRECISION, s6 DOUBLE PRECISION, s7 DOUBLE PRECISION, s8 DOUBLE PRECISION, s9 DOUBLE PRECISION,
        s10 DOUBLE PRECISION, s11 DOUBLE PRECISION, s12 DOUBLE PRECISION, s13 DOUBLE PRECISION, s14 DOUBLE PRECISION,
        s15 DOUBLE PRECISION, s16 DOUBLE PRECISION, s17 DOUBLE PRECISION, s18 DOUBLE PRECISION, s19 DOUBLE PRECISION,
        s20 DOUBLE PRECISION, s21 DOUBLE PRECISION, s22 DOUBLE PRECISION, s23 DOUBLE PRECISION, s24 DOUBLE PRECISION,
        s25 DOUBLE PRECISION, s26 DOUBLE PRECISION, s27 DOUBLE PRECISION, s28 DOUBLE PRECISION, s29 DOUBLE PRECISION,
        s30 DOUBLE PRECISION, s31 DOUBLE PRECISION, s32 DOUBLE PRECISION, s33 DOUBLE PRECISION, s34 DOUBLE PRECISION,
        s35 DOUBLE PRECISION, s36 DOUBLE PRECISION, s37 DOUBLE PRECISION, s38 DOUBLE PRECISION, s39 DOUBLE PRECISION,
        s40 DOUBLE PRECISION, s41 DOUBLE PRECISION, s42 DOUBLE PRECISION, s43 DOUBLE PRECISION, s44 DOUBLE PRECISION,
        s45 DOUBLE PRECISION, s46 DOUBLE PRECISION, s47 DOUBLE PRECISION, s48 DOUBLE PRECISION, s49 DOUBLE PRECISION,
        s50 DOUBLE PRECISION, s51 DOUBLE PRECISION, s52 DOUBLE PRECISION, s53 DOUBLE PRECISION, s54 DOUBLE PRECISION,
        s55 DOUBLE PRECISION, s56 DOUBLE PRECISION, s57 DOUBLE PRECISION, s58 DOUBLE PRECISION, s59 DOUBLE PRECISION,
        s60 DOUBLE PRECISION, s61 DOUBLE PRECISION, s62 DOUBLE PRECISION, s63 DOUBLE PRECISION, s64 DOUBLE PRECISION,
        s65 DOUBLE PRECISION, s66 DOUBLE PRECISION, s67 DOUBLE PRECISION, s68 DOUBLE PRECISION, s69 DOUBLE PRECISION,
        s70 DOUBLE PRECISION, s71 DOUBLE PRECISION, s72 DOUBLE PRECISION, s73 DOUBLE PRECISION, s74 DOUBLE PRECISION,
        s75 DOUBLE PRECISION, s76 DOUBLE PRECISION, s77 DOUBLE PRECISION, s78 DOUBLE PRECISION, s79 DOUBLE PRECISION,
        s80 DOUBLE PRECISION, s81 DOUBLE PRECISION, s82 DOUBLE PRECISION, s83 DOUBLE PRECISION, s84 DOUBLE PRECISION,
        s85 DOUBLE PRECISION, s86 DOUBLE PRECISION, s87 DOUBLE PRECISION, s88 DOUBLE PRECISION, s89 DOUBLE PRECISION,
        s90 DOUBLE PRECISION, s91 DOUBLE PRECISION, s92 DOUBLE PRECISION, s93 DOUBLE PRECISION, s94 DOUBLE PRECISION,
        s95 DOUBLE PRECISION, s96 DOUBLE PRECISION, s97 DOUBLE PRECISION, s98 DOUBLE PRECISION, s99 DOUBLE PRECISION
    );"

    # Create a hypertable in TimescaleDB
    docker exec -it timescaledb-container psql -U postgres -c "SELECT create_hypertable('$dataset', 'time', chunk_time_interval=>'7 days'::INTERVAL);"

    # Load data into the table
    docker exec -u 0 -it timescaledb-container psql -U postgres -c "\copy $dataset FROM '/var/lib/postgresql/data/TSM-Bench/compression/datasets/$dataset.csv' DELIMITER ',' CSV HEADER;"

    # Wait for the data to be fully loaded
    sleep 10

    # Compute compression for the dataset
#    compression_output=$(docker exec -it timescaledb-container psql -U postgres -c "SELECT hypertable_size('$dataset');")
	compression_output=$(docker exec -it timescaledb-container psql -U postgres -c "SELECT table_name, pg_size_pretty(hypertable_size('$dataset')) AS size FROM information_schema.tables WHERE table_schema='public' AND table_name='$dataset';")



    # Print compression information
    echo "$compression_output"

    # Append compression results to output file
    results_dir="../results/compression"
    mkdir -p "$results_dir"
    output_file="$results_dir/time_and_compression.txt"
    echo "$compression_output" >> "$output_file"
}

# Restart TimescaleDB container
restart_timescaledb

# Iterate through all CSV files in the folder and load them
for file in "$folder_path"/*.csv; do
    if [ -f "$file" ]; then
        load_dataset "$file"
    fi
done

# Stop TimescaleDB container
docker stop "$container_name"