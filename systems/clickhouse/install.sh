#!/bin/sh


sudo kill -9 `sudo lsof -t -i:9000`
sleep 2

sudo pip3 install clickhouse-driver

sudo docker pull clickhouse/clickhouse-server

sudo docker run -d --name clickhouse-container \
	-p 8123:8123 -p 9000:9000 \
	clickhouse/clickhouse-server
	
sleep 5
sudo docker stop clickhouse-container

# # loading 
# time ( cat '../../Datasets/d1.csv' | sudo docker exec -i clickhouse-container clickhouse-client --format_csv_delimiter="," --query="INSERT INTO d1 FORMAT CSVWithNames" ) 




# compression



# sudo docker cp config.xml clickhouse-container:/etc/clickhouse-server/

# sudo kill -9 $(lsof -t -i:9000)

