#!/bin/sh

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3-venv
sudo apt-get install -y python3.8-venv
sudo apt-get install -y libpython3.8-dev
sudo apt-get install -y python3-dev
sudo apt-get install -y build-essential
sudo apt-get install -y unzip

python3.8 -m venv TSMvenv
. TSMvenv/bin/activate
python3.8 -m pip install --upgrade pip
# Python3.8 (the extremdb installation settup requires to build a 3.8 wheel)

pip3 install saxpy
pip3 install numpy
pip3 install pandas
pip3 install protobuf==3.13.0
pip3 install tqdm
pip3 install gdown
pip3 install pylab-sdk
pip3 install sqlalchemy
pip3 install matplotlib
pip3 install matplotlib_terminal
pip3 install pandas
pip3 install jsonlines
pip3 install lshashpy3

sudo apt-get install  libpq-dev -y
pip3 install psycopg2
pip3 install pymonetdb

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
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version


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
current_user=$(whoami)
sudo usermod -aG docker "$current_user"
newgrp docker
sudo chmod 666 /var/run/docker.sock
