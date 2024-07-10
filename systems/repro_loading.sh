#!/bin/sh

# List of systems
systems="clickhouse druid extremedb influx monetdb questdb timescaledb"

# Base directory containing system directories
base_dir=$(dirname "$0")  # Get the directory of the script (assuming script is in systems/)

# Output file path
output_file="$base_dir/../results/loading.txt"

# Ensure the output directory exists, create if not
mkdir -p "$base_dir/../results"
touch "$output_file"

# Function to read and parse data from each system's file
parse_results() {
    system_dir="$base_dir/$1"
    file_path="$system_dir/time_and_compression.txt"

    if [ -f "$file_path" ]; then
        while IFS= read -r line; do
            dataset_name=$(echo "$line" | awk '{print $1}')
            storage=$(echo "$line" | awk '{print $2}')
            loading_time=$(echo "$line" | awk '{print $3}')
            
            # Append formatted output for each line to the output file
            echo "$dataset_name,$1,$storage,$loading_time" >> "$output_file"
            echo "$dataset_name,$1,$storage,$loading_time"
        done < "$file_path"
    fi
}

# Iterate through each system and parse the results
for system in $systems; do
    parse_results "$system"
done
