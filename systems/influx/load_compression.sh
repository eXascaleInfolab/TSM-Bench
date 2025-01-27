#!/bin/sh

# Launch InfluxDB
sh launch.sh

folder="datasets_influx"
if [ $# -ge 1 ]; then
    folder="$1"
fi

echo "Processing folder: $folder"

# Initialize the output file
results_dir="../../results/compression"
mkdir -p "$results_dir"
output_file="$results_dir/time_and_compression.txt"

echo "### InfluxDB" >> $output_file
echo "Dataset_name,Size" >> $output_file

for file_path in "$folder"/*-influxdb.csv; do
    # Extract the dataset name from the file
    dataset=$(basename "$file_path" "-influxdb.csv")
    echo "Processing dataset: $dataset"

    # Drop the existing database if it exists
    curl -X POST "http://localhost:8086/query" --data-urlencode "q=DROP DATABASE $dataset"

    log_file="influx_startup_$dataset.txt"
    start_time=$(date +%s.%N)

    # Load the dataset into InfluxDB
    ./influxdb-1.7.10-1/usr/bin/influx -import -path="$file_path" -precision=ms > "$log_file" 2>&1 &

    echo "Start loading $dataset"

    # Monitor log file for errors
    last_line=0
    while : ; do
        current_lines=$(awk 'END {print NR}' "$log_file")

        if [ "$current_lines" -gt "$last_line" ]; then
            sed -n "$((last_line + 1)),$current_lines p" "$log_file"
            last_line="$current_lines"

            # Check for failure messages
            if grep -q "Failed" "$log_file"; then
                echo "Failed message detected for $dataset! Exiting..."
                break
            fi
        fi
        sleep 5
    done
    rm "$log_file"

    end_time=$(date +%s.%N)
    elapsed_time=$(echo "$end_time - $start_time" | bc)

    # Get the size of the file
    file_size=$(du -sh "$file_path" | cut -f1)
    echo "$dataset,$file_size" >> $output_file

    echo "Compression: $file_size"
    echo "$dataset loaded in ${elapsed_time}s"
done

echo "DONE"
