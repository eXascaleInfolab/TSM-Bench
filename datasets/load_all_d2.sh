#!/bin/sh

dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi
echo "loading $dataset"

cd ../systems

sh stop_all.sh


echo "loading data into MonetDB"
# MonetDB
cd monetdb
sh ./load.sh $dataset
cd ..

echo "loading data into QuestDB"
# QuestDB
cd questdb
sh ./load.sh $dataset
cd ..

