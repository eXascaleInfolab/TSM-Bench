#!/bin/sh



sudo touch /etc/apt/sources.list.d/monetdb.list
sudo chmod 777 /etc/apt/sources.list.d/monetdb.list
echo "deb https://dev.monetdb.org/downloads/deb/ $(lsb_release -cs) monetdb" >> /etc/apt/sources.list.d/monetdb.list
echo "deb-src https://dev.monetdb.org/downloads/deb/ $(lsb_release -cs) monetdb" >> /etc/apt/sources.list.d/monetdb.list
wget --output-document=- https://www.monetdb.org/downloads/MonetDB-GPG-KEY | sudo apt-key add -
sudo apt update
wget https://www.monetdb.org/downloads/sources/Nov2019-SP3/MonetDB-11.35.19.zip
sudo apt install -y unzip
unzip MonetDB-11.35.19.zip
sudo rm -rf MonetDB-11.35.19.zip
cd MonetDB-11.35.19/
echo "installing dependencies..."
sudo apt install -y automake bison gettext libssl-dev libtool libxml2-dev m4 make mercurial pkg-config
sudo apt install -y libatomic-ops-dev python-dev python-numpy uuid-dev
sudo ./bootstrap
sudo ./configure --enable-pyintegration
sudo make
sudo make install
echo "installing monetdb client..."
sudo apt install -y monetdb-client
sudo rm install 

filename=~/.monetdb
if [ ! -f $filename ]
then
    rm -rf $filename
    touch $filename
    echo 'user=monetdb' >> $filename
    echo 'password=monetdb' >> $filename
fi

sudo monetdbd stop master_db
sudo rm -rf master_db/
sudo monetdbd create master_db
sudo set listenaddr=0.0.0.0 master_db
sudo monetdbd set port=54320 master_db
sudo monetdbd start master_db
sudo monetdb create mydb
sudo monetdb release mydb
sudo monetdb set embedpy3=yes mydb
