# BY default quest dbs root directory is inside your home direcctory "https://questdb.io/docs/reference/command-line-options/"  IF change it fi you run ot of space
# questdb.sh start -d "$system_directory" specifies the directory path, this also has to be updated inside questdb/launch.sh

system_directory="/localdata/.questdb"


sudo kill -9 `sudo lsof -t -i:9000`
sleep 2

wget https://github.com/questdb/questdb/releases/download/6.4.1/questdb-6.4.1-rt-linux-amd64.tar.gz


tar -xf questdb-6.4.1-rt-linux-amd64.tar.gz
rm questdb-6.4.1-rt-linux-amd64.tar.gz

mkdir "$system_directory"
mkdir "$system_directory/conf/"
cp server.conf $system_directory/conf/

./questdb-6.4.1-rt-linux-amd64/bin/questdb.sh start -d "$system_directory"

sleep 25
