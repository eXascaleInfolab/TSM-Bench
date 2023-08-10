#!/bin/bash


tar xvzf extremedb_8.3_fusion_linux_x86_64_sql_lua_eval.tar.gz 

cd eXtremeDB/
make all
cd target/python/
python3 setup.py install --user


cd ../../..
cp xsql.cfg eXtremeDB/target/bin
cp create.sql eXtremeDB/target/bin

sudo cp -r eXremeDB/target/bin.so/ /usr/

sudo apt-get update -y
sudo apt-get install -y libreadline-dev

pip3 install --force-reinstall eXtremeDB/target/python/dist/exdb_mcobject-0.1.1-cp36-cp36m-linux_x86_64.whl 
# 
current="$(pwd)"

export MCO_ROOT="$current"/systems/eXtremeDB/
export MCO_LIBRARY_PATH="$current"/systems/eXtremeDB/target/bin.so
export LD_LIBRARY_PATH="$current"/systems/eXtremeDB/target/bin.so


# export MCO_PYTHONAPILIB=/home/abdel/.local/lib/python3.8/site-packages/exdb_mcobject-0.1.1-py3.8-linux-x86_64.egg/exdb/libmcopythonapi.so

# export MCO_ROOT=/path/to/extremeDB
# export MCO_LIBRARY_PATH=/path/to/eXtremeDB/target/bin.so
# export LD_LIBRARY_PATH=/path/to/eXtremeDB/target/bin.so

# export MCO_ROOT=/localdata/ABench-IoT/Databases/extremedb/eXtremeDB/target/bin.so/
# export LD_LIBRARY_PATH=/localdata/ABench-IoT/Databases/extremedb/eXtremeDB/target/bin.so/
# export MCO_LIBRARY_PATH=/localdata/ABench-IoT/Databases/extremedb/eXtremeDB/target/bin.so/
# export MCO_PYTHONAPILIB=/home/abdel/.local/lib/python3.8/site-packages/exdb_mcobject-0.1.1-py3.8-linux-x86_64.egg/exdb/libmcopythonapi.so
# export MCO_PYTHONAPILIB=/home/abdel/.local/lib/python3.8/site-packages/exdb_mcobject-0.1.1-py3.8-linux-x86_64.egg/exdb/libmcopythonapi.so 
