#!/bin/sh

sudo apt update

# Python3.X
sudo apt install -y python3
sudo apt install -y python3-pip
sudo pip3 install saxpy
sudo pip3 install numpy
sudo pip3 install pydruid
sudo pip3 install pandas
sudo pip3 install protobuf==3.13.0
sudo pip3 install tqdm
sudo pip3 install gdown
sudo pip3 install pylab-sdk

# Java
sudo apt-get install -y openjdk-8-jdk
sudo update-java-alternatives --jre-headless --jre --set java-1.8.0-openjdk-amd64

# Maven
sudo apt install -y maven

# Curl
sudo apt install -y curl

# Docker
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# ClickHouse
cd clickhouse
sh ./install.sh
cd ..

# Druid
cd druid
sh ./install.sh
cd ..

# ExtremeDB
cd extremedb
source ./install.sh
cd ..

# Influx
cd influx
sh ./install.sh
cd ..

# MonetDB
cd monetdb
sh ./install.sh
cd ..


# QuestDB
cd questdb
sh ./install.sh
cd ..

# TimescaleDB
cd  timescaledb
sh ./install.sh
cd ..