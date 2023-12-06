#!/bin/bash

compression_folder="compression"
systems_to_load_compression=("clickhouse" "druid" "influx" "timescaledb")

echo "starting compression computation"

# Get a list of files in the compression folder
compression_datasets=$(ls "$compression_folder")

cp "$compression_folder"/* .

cd "../systems" || exit

# Track the originally compressed files
original_compression_files=("$compression_datasets")

# Iterate over each system in the list
for system in "${systems_to_load_compression[@]}"; do
  # Move to the system directory
  cd "$system" || exit
  echo "$system"
  # Iterate over each data file in the compression folder
  for data_file in $original_compression_files; do
    # Load the data using the load script (assuming the script is named load.sh)
    sh load.sh "${data_file%.csv}"  # Remove the .csv extension
  done

  # Move back to the parent directory
  cd ..
done

# Move only the originally compressed files back to the compression folder
for file in "${original_compression_files[@]}"; do
  mv "$file" "../$compression_folder/"
done


# Remove the compression datasets in this folder on error or termination
cd "datasets"
rm -f $original_compression_files
