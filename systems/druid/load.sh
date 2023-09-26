#!/bin/sh

# THE FOLLOWING SCRIPT WILL SETUP AND LOAD D1, TO LOAD D2 UNCOMMENT THE LINES BELOW


current=$(pwd)

dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi
echo "loading $dataset"


echo "start!"

sed "s/d1/$dataset/g" load_template.json > temp_template.json

sed 's?path_to_file?'`pwd`/../../datasets/$dataset.csv'?' temp_template.json > load.json
echo "load json"

rm temp_template.json


sh launch.sh
echo "wait for launch"


start_time=$(date +%s.%N)


log_file="druid_startup.txt"

# Start the Apache Druid server and redirect its output to the log file
./apache-druid-25.0.0/bin/post-index-task --file load.json --url http://localhost:8081 > "$log_file" 2>&1 &

echo "start loading"

# Initialize the last_line variable
last_line=0

# Continuously monitor the log file for new lines
while : ; do
  # Get the current line count
  current_lines=$(awk 'END {print NR}' "$log_file")
  
  echo "$current_lines"
  
  # Check if there are new lines since the last check
  if [ "$current_lines" -gt "$last_line" ]; then
    # Print the new lines
    sed -n "$((last_line + 1)),$current_lines p" "$log_file"

    # Update the last_line variable
    last_line="$current_lines"
    
    # Check if any line in the new lines contains "failed"
    if grep -q "failed" "$log_file"; then
      echo "Failed message detected! Exiting..."
      break  # Exit the loop when "failed" is found
    fi

    if grep -q "loading complete!" "$log_file"; then
      echo "loading complete! Exiting..."
      break  # Exit the loop when "failed" is found
    fi
  fi

  sleep 10  # Wait for a few seconds before checking again
done
rm $log_file

end_time=$(date +%s.%N)
elapsed_time=$(echo "$end_time - $start_time" | bc)
echo "Loading time: $elapsed_time seconds" > loading_time_$dataset.txt
echo $elapsed_time


echo "load database"
#du -sh ./apache-druid-25.0.0/var/druid/segment-cache/d1


echo "data loading finished"

## uncoment the following for D2 ##
###################################
# echo "start loading!"
#sed 's?path_to_file?'`pwd`/../../datasets/d2.csv'?' load_template.json > load.json
#echo "load json"
#time ./apache-druid-25.0.0/bin/post-index-task --file load.json --url http://localhost:8081 &
