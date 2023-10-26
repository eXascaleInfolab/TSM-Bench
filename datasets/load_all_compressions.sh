#!/bin/bash


compression_folder="compression"

# Iterate over files in the compression folder
for full_path in "$compression_folder"/*.csv; do
    if [ -e "$full_path" ]; then
        # Extract the file name without the full path and the .csv extension
        file_name_without_extension=$(basename "$full_path" .csv)

        # Step 1: Move the file to the current directory
        mv "$full_path" "$file_name_without_extension.csv"
        
        # Step 2: Execute the shell script with dataset name (without .csv)
        sh load_all.sh "$file_name_without_extension"
        
        # Step 3: Move the file back to the compression folder
        mv "$file_name_without_extension.csv" "$full_path"
    fi
done




