#!/bin/sh

sudo docker stop questdb-container
sudo docker rm questdb-container 
sudo docker pull questdb/questdb:6.6.1
sudo docker run -d -p 9000:9000 \
        --name questdb-container \
        -v "$pwd:/var/lib/questdb" \
        questdb/questdb:6.6.1
sudo docker stop questdb-container

#wget https://github.com/questdb/questdb/releases/download/6.6.1/questdb-6.6.1-rt-linux-amd64.tar.gz

#tar -xf questdb-6.6.1-rt-linux-amd64.tar.gz
#rm questdb-6.6.1-rt-linux-amd64.tar.gz

#cp server.conf ../../../../.questdb/conf/
#sudo cp server.conf /root/.questdb/conf/

# sudo ./questdb.sh start
