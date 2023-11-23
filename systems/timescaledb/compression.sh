#!/bin/sh

# THE FOLLOWING SCRIPT WILL PRINT STORAGE SIZE FOR D1, TO SHOW D2 UNCOMMENT THE LINES BELOW
dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi


#docker start timescaledb-container


sleep 15

output=$( docker exec -it timescaledb-container psql -U postgres -c "SELECT hypertable_size('$dataset') ;")
echo "storing"
echo "$output"
number=$(echo "$output" | awk 'NR==3 {print $1}')
number=$((number))

echo "$number"

#divisor=1000000
#result=$(echo "scale=2; $number / $divisor" | bc)
result=$number

echo "result"
echo "${result}B" 


#mute=$(sudo docker stop timescaledb-container) 
