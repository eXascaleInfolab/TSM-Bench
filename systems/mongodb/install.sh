#!/bin/sh

sudo docker pull mongodb/mongodb-community-server
sudo docker run --name mongo -d mongodb/mongodb-community-server:latest

pip3 install pymongo

sudo docker stop mongo 

sudo docker start mongo 

sudo docker restart mongo
