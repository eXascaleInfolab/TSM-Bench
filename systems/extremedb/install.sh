#!/bin/bash


 tar xvzf extremedb_8.3_fusion_linux_x86_64_sql_lua_eval.tar.gz 

# export MCO_ROOT="$current"/eXtremeDB/
export MCO_LIBRARY_PATH="$current"/eXtremeDB/target/bin.so
export LD_LIBRARY_PATH="$current"/eXtremeDB/target/bin.so

cd eXtremeDB/
make all
cd target/python/
python3 setup.py install --user


cd ../../..
cp xsql.cfg eXtremeDB/target/bin
#cp create.sql eXtremeDB/target/bin

sudo cp -r eXremeDB/target/bin.so/ /usr/

sudo apt-get update -y
sudo apt-get install -y libreadline-dev

pip3 install --force-reinstall eXtremeDB/target/python/dist/exdb_mcobject-0.1.1-cp38-cp38-linux_x86_64.whl

current="$(pwd)"

export MCO_ROOT="$current"/eXtremeDB/
export MCO_LIBRARY_PATH="$current"/eXtremeDB/target/bin.so
export LD_LIBRARY_PATH="$current"/eXtremeDB/target/bin.so


