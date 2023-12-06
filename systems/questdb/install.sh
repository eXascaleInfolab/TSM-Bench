# BY default quest dbs root directory is inside your home direcctory "https://questdb.io/docs/reference/command-line-options/"  IF change it fi you run ot of space
# questdb.sh  change the QuestDBroot inside systems/config.env

. ../config.env

sudo kill -9 `sudo lsof -t -i:9000`
sleep 2

wget https://github.com/questdb/questdb/releases/download/6.4.1/questdb-6.4.1-rt-linux-amd64.tar.gz


tar -xf questdb-6.4.1-rt-linux-amd64.tlsar.gz
rm questdb-6.4.1-rt-linux-amd64.tar.gz

mkdir "$QuestDBroot"
mkdir "$QuestDBroot/conf/"
cp server.conf "$QuestDBroot/conf/"

./questdb-6.4.1-rt-linux-amd64/bin/questdb.sh start -d "$QuestDBroot"

sleep 25
