#!/bin/sh


current="$(pwd)"

export MCO_ROOT="$current"
export MCO_LIBRARY_PATH="$current"/eXtremeDB/target/bin.so
export LD_LIBRARY_PATH="$current"/eXtremeDB/target/bin.so

# export MCO_PYTHONAPILIB=/home/abdel/.local/lib/python3.8/site-packages/exdb_mcobject-0.1.1-py3.8-linux-x86_64.egg/exdb/libmcopythonapi.so

# export MCO_ROOT=/path/to/extremeDB
# export MCO_LIBRARY_PATH=/path/to/eXtremeDB/target/bin.so
# export LD_LIBRARY_PATH=/path/to/eXtremeDB/target/bin.so

# export MCO_ROOT=/localdata/ABench-IoT/Databases/extremedb/eXtremeDB/target/bin.so/
# export LD_LIBRARY_PATH=/localdata/ABench-IoT/Databases/extremedb/eXtremeDB/target/bin.so/
# export MCO_LIBRARY_PATH=/localdata/ABench-IoT/Databases/extremedb/eXtremeDB/target/bin.so/
# export MCO_PYTHONAPILIB=/home/abdel/.local/lib/python3.8/site-packages/exdb_mcobject-0.1.1-py3.8-linux-x86_64.egg/exdb/libmcopythonapi.so
# export MCO_PYTHONAPILIB=/home/abdel/.local/lib/python3.8/site-packages/exdb_mcobject-0.1.1-py3.8-linux-x86_64.egg/exdb/libmcopythonapi.so 