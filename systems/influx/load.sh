#!/bin/sh

# THE FOLLOWING SCRIPT WILL SETUP AND LOAD D1, TO LOAD D2 UNCOMMENT THE LINES BELOW 
sh launch.sh

dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi
echo $dataset

echo "convert the datase tformat (this takes a while and is not counted in the time measuring)"
python3 generate_influx_line_protocol.py $dataset


curl -X POST "http://localhost:8086/query" --data-urlencode "q=DROP DATABASE $dataset"

log_file="influx_startup.txt"
start_time=$(date +%s.%N)


./influxdb-1.7.10-1/usr/bin/influx -import -path=$dataset-influxdb.csv -precision=ms > "$log_file" 2>&1 &

echo "start loading"

# Initialize the last_line variJasable
last_line=0

# Continuously monitor the log file for new lines
while : ; do
  # Get the current line count
  current_lines=$(awk 'END {print NR}' "$log_file")

  #echo "$current_lines"

  # Check if there are new lines since the last check
  if [ "$current_lines" -gt "$last_line" ]; then
    # Print the new lines
    sed -n "$((last_line + 1)),$current_lines p" "$log_file"

    # Update the last_line variable
    last_line="$current_lines"

    # Check if any line in the new lines contains "failed"
    if grep -q "Failed" "$log_file"; then
      echo "Final message detected! Exiting..."
      break  # Exit the loop when "failed" is found
    fi

  fi

  sleep 5  # Wait for a few seconds before checking again
done
rm $log_file

end_time=$(date +%s.%N)
elapsed_time=$(echo "$end_time - $start_time" | bc)
echo $elapsed_time

compression=$(sh compression.sh $dataset)

echo "Compression: $compression"
echo "$dataset $compression ${elapsed_time}s" >> time_and_compression.txt



echo "DONE"
