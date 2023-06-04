# Thesis

___
## Prerequisites and dependencies

- Ubuntu 18 or higher
- Clone this repository
- All other dependencies will be installed via the install script.

___
## Install

To install all components, there is an install script provided for both the Databases and Datasets:

```bash
cd Databases
sh install_all.sh
cd ../Datasets/
sh install.sh
```

For installing one particular database, then go to the directory of that database in the Databases directory and run the install script there. For example,

```bash
cd Databases/influx
sh install.sh
```
___
## Running evals

| Database | Algorithm | Datasets |
| ------ | ------ | ------ |
| extremedb | cd| weather |
| monetdb | dist | monitoring |
| timescaledb | dstree | activity |
| influx | hotsax |  medical |
| graphite | kmeans | <custom_path_to_file> |
| kairosdb-cassandra | knn | |
| kairosdb-h2 | knn-operators | |
| druid | records-select-long | |
| | recovdb | |
| | sax-representation | |
| | screen | |
| | simple-queries | |
| | sum-long | |
| | z-normalization | |
| | z-normalization-operators | |

Please note that not all combination work. The script will warn you when trying to run an invalid combination.

The limits of the datasets are the following:

| Dataset | # of TS | Length of TS |
| ------ | ------ | ------ |
| weather | 46| 3,500,000 |
| activity | 360 | 142,500 |
| medical | 512 | 7,000 |
| monitoring | 43,680 |  2,205 |



___
## Running evals based on figures in the work

Insert time and throughput is taken for each run. It is a double check that the data has been inserted

##### FIGURE 4.5 Simple queries(QA).

QA.1, QA.2

```bash
python3 run_eval.py --dataset weather --lines 3000000 --algorithm simple-queries --database influx
python3 run_eval.py --dataset weather --lines 3000000 --algorithm simple-queries --database timescaledb
python3 run_eval.py --dataset weather --lines 3000000 --algorithm simple-queries --database monetdb
python3 run_eval.py --dataset weather --lines 3000000 --algorithm simple-queries --database extremedb
python3 run_eval.py --dataset weather --lines 3000000 --algorithm simple-queries --database graphite
python3 run_eval.py --dataset weather --lines 3000000 --algorithm simple-queries --database kairosdb-h2
python3 run_eval.py --dataset weather --lines 3000000 --algorithm simple-queries --database kairosdb-cassandra
python3 run_eval.py --dataset weather --lines 3000000 --algorithm simple-queries --database druid
```

QA.3

```bash
python3 run_eval.py --dataset weather --lines 1000000 --algorithm simple-queries --database influx
python3 run_eval.py --dataset weather --lines 1000000 --algorithm simple-queries --database timescaledb
python3 run_eval.py --dataset weather --lines 1000000 --algorithm simple-queries --database monetdb
python3 run_eval.py --dataset weather --lines 1000000 --algorithm simple-queries --database extremedb
python3 run_eval.py --dataset weather --lines 1000000 --algorithm simple-queries --database graphite
python3 run_eval.py --dataset weather --lines 1000000 --algorithm simple-queries --database kairosdb-h2
python3 run_eval.py --dataset weather --lines 1000000 --algorithm simple-queries --database kairosdb-cassandra
```

QA.4

```bash
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm dist --database influx
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm dist --database timescaledb
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm dist --database monetdb
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm dist --database extremedb
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm dist --database graphite
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm dist --database druid
```

##### FIGURE 4.6 Simple queries(QA) on a large dataset.

Records

```bash
python3 run_eval.py --dataset monitoring --lines 2205 --columns 20000 --algorithm records-select-long --database influx
python3 run_eval.py --dataset monitoring --lines 2205 --columns 20000 --algorithm records-select-long --database timescaledb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 20000 --algorithm records-select-long --database monetdb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 20000 --algorithm records-select-long --database extremedb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 20000 --algorithm records-select-long --database graphite
python3 run_eval.py --dataset monitoring --lines 2205 --columns 20000 --algorithm records-select-long --database kairosdb-h2
python3 run_eval.py --dataset monitoring --lines 2205 --columns 20000 --algorithm records-select-long --database kairosdb-cassandra
```

RecordsSum

```bash
python3 run_eval.py --dataset monitoring --lines 2205 --columns 5000 --algorithm sum-long --database influx
python3 run_eval.py --dataset monitoring --lines 2205 --columns 5000 --algorithm rsum-long --database timescaledb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 5000 --algorithm sum-long --database monetdb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 5000 --algorithm sum-long --database extremedb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 5000 --algorithm sum-long --database graphite
```

##### FIGURE 4.7 Runtime of Z-Normalization (QB1)

Weather

```bash
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm z-normalization --database influx
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm z-normalization --database timescaledb
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm z-normalization --database monetdb
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm z-normalization --database extremedb
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm z-normalization --database graphite
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm z-normalization --database kairosdb-h2
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm z-normalization --database kairosdb-cassandra
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm z-normalization --database druid
```

Activity

```bash
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm z-normalization --database influx
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm z-normalization --database timescaledb
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm z-normalization --database monetdb
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm z-normalization --database extremedb
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm z-normalization --database graphite
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm z-normalization --database kairosdb-h2
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm z-normalization --database kairosdb-cassandra
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm z-normalization --database druid
```

Medical

```bash
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm z-normalization --database influx
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm z-normalization --database timescaledb
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm z-normalization --database monetdb
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm z-normalization --database extremedb
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm z-normalization --database graphite
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm z-normalization --database kairosdb-h2
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm z-normalization --database kairosdb-cassandra
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm z-normalization --database druid
```

Monitoring

```bash
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm z-normalization --database influx
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm z-normalization --database timescaledb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm z-normalization --database monetdb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm z-normalization --database extremedb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm z-normalization --database graphite
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm z-normalization --database kairosdb-h2
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm z-normalization --database kairosdb-cassandra
```

##### FIGURE 4.7 Runtime of Z-Normalization (QB1) using Database operators

Weather

```bash
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm z-normalization-operators --database influx
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm z-normalization-operators --database timescaledb
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm z-normalization-operators --database monetdb
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm z-normalization-operators --database extremedb
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm z-normalization-operators --database graphite
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm z-normalization-operators --database
```

##### FIGURE 4.9 Runtime of SAX representation (QB2).

Weather

```bash
python3 run_eval.py --dataset weather --lines 750000 --columns 46 --algorithm sax-representation --database influx
python3 run_eval.py --dataset weather --lines 750000 --columns 46 --algorithm sax-representation --database timescaledb
python3 run_eval.py --dataset weather --lines 750000 --columns 46 --algorithm sax-representation --database monetdb
python3 run_eval.py --dataset weather --lines 750000 --columns 46 --algorithm sax-representation --database extremedb
python3 run_eval.py --dataset weather --lines 750000 --columns 46 --algorithm sax-representation --database graphite
python3 run_eval.py --dataset weather --lines 750000 --columns 46 --algorithm sax-representation --database kairosdb-h2
python3 run_eval.py --dataset weather --lines 750000 --columns 46 --algorithm sax-representation --database kairosdb-cassandra
python3 run_eval.py --dataset weather --lines 750000 --columns 46 --algorithm sax-representation --database druid
```

Activity

```bash
python3 run_eval.py --dataset activity --lines 90000 --columns 360 --algorithm sax-representation --database influx
python3 run_eval.py --dataset activity --lines 90000 --columns 360 --algorithm sax-representation --database timescaledb
python3 run_eval.py --dataset activity --lines 90000 --columns 360 --algorithm sax-representation --database monetdb
python3 run_eval.py --dataset activity --lines 90000 --columns 360 --algorithm sax-representation --database extremedb
python3 run_eval.py --dataset activity --lines 90000 --columns 360 --algorithm sax-representation --database graphite
python3 run_eval.py --dataset activity --lines 90000 --columns 360 --algorithm sax-representation --database kairosdb-h2
python3 run_eval.py --dataset activity --lines 90000 --columns 360 --algorithm sax-representation --database kairosdb-cassandra
python3 run_eval.py --dataset activity --lines 90000 --columns 360 --algorithm sax-representation --database druid
```

Medical

```bash
python3 run_eval.py --dataset medical --lines 6000 --columns 512 --algorithm sax-representation --database influx
python3 run_eval.py --dataset medical --lines 6000 --columns 512 --algorithm sax-representation --database timescaledb
python3 run_eval.py --dataset medical --lines 6000 --columns 512 --algorithm sax-representation --database monetdb
python3 run_eval.py --dataset medical --lines 6000 --columns 512 --algorithm sax-representation --database extremedb
python3 run_eval.py --dataset medical --lines 6000 --columns 512 --algorithm sax-representation --database graphite
python3 run_eval.py --dataset medical --lines 6000 --columns 512 --algorithm sax-representation --database kairosdb-h2
python3 run_eval.py --dataset medical --lines 6000 --columns 512 --algorithm sax-representation --database kairosdb-cassandra
python3 run_eval.py --dataset medical --lines 6000 --columns 512 --algorithm sax-representation --database druid
```

Monitoring

```bash
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm sax-representation --database influx
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm sax-representation --database timescaledb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm sax-representation --database monetdb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm sax-representation --database extremedb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm sax-representation --database graphite
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm sax-representation --database kairosdb-h2
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm sax-representation --database kairosdb-cassandra
```



##### FIGURE 4.10 Runtime of Centroid Decomposition (QB3).

Weather

```bash
python3 run_eval.py --dataset weather --lines 100000 --columns 46 --algorithm cd --database influx
python3 run_eval.py --dataset weather --lines 100000 --columns 46 --algorithm cd --database timescaledb
python3 run_eval.py --dataset weather --lines 100000 --columns 46 --algorithm cd --database monetdb
python3 run_eval.py --dataset weather --lines 100000 --columns 46 --algorithm cd --database extremedb
python3 run_eval.py --dataset weather --lines 100000 --columns 46 --algorithm cd --database graphite
python3 run_eval.py --dataset weather --lines 100000 --columns 46 --algorithm cd --database kairosdb-h2
python3 run_eval.py --dataset weather --lines 100000 --columns 46 --algorithm cd --database kairosdb-cassandra
python3 run_eval.py --dataset weather --lines 100000 --columns 46 --algorithm cd --database druid
```

Activity

```bash
python3 run_eval.py --dataset activity --lines 10000 --columns 360 --algorithm cd --database influx
python3 run_eval.py --dataset activity --lines 10000 --columns 360 --algorithm cd --database timescaledb
python3 run_eval.py --dataset activity --lines 10000 --columns 360 --algorithm cd --database monetdb
python3 run_eval.py --dataset activity --lines 10000 --columns 360 --algorithm cd --database extremedb
python3 run_eval.py --dataset activity --lines 10000 --columns 360 --algorithm cd --database graphite
python3 run_eval.py --dataset activity --lines 10000 --columns 360 --algorithm cd --database kairosdb-h2
python3 run_eval.py --dataset activity --lines 10000 --columns 360 --algorithm cd --database kairosdb-cassandra
python3 run_eval.py --dataset activity --lines 10000 --columns 360 --algorithm cd --database druid
```

Medical

```bash
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm cd --database influx
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm cd --database timescaledb
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm cd --database monetdb
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm cd --database extremedb
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm cd --database graphite
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm cd --database kairosdb-h2
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm cd --database kairosdb-cassandra
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm cd --database druid
```

Monitoring

```bash
python3 run_eval.py --dataset monitoring --lines 500 --columns 6000 --algorithm cd --database influx
python3 run_eval.py --dataset monitoring --lines 500 --columns 6000 --algorithm cd --database timescaledb
python3 run_eval.py --dataset monitoring --lines 500 --columns 6000 --algorithm cd --database monetdb
python3 run_eval.py --dataset monitoring --lines 500 --columns 6000 --algorithm cd --database extremedb
python3 run_eval.py --dataset monitoring --lines 500 --columns 6000 --algorithm cd --database graphite
python3 run_eval.py --dataset monitoring --lines 500 --columns 6000 --algorithm cd --database kairosdb-h2
python3 run_eval.py --dataset monitoring --lines 500 --columns 6000 --algorithm cd --database kairosdb-cassandra
python3 run_eval.py --dataset monitoring --lines 500 --columns 6000 --algorithm cd --database druid
```



##### FIGURE 4.11 Runtime of recovery of missing values (QB4).

Weather

```bash
python3 run_eval.py --dataset weather --lines 100000 --columns 46 --algorithm recovdb --database influx
python3 run_eval.py --dataset weather --lines 100000 --columns 46 --algorithm recovdb --database timescaledb
python3 run_eval.py --dataset weather --lines 100000 --columns 46 --algorithm recovdb --database monetdb
python3 run_eval.py --dataset weather --lines 100000 --columns 46 --algorithm recovdb --database extremedb
python3 run_eval.py --dataset weather --lines 100000 --columns 46 --algorithm recovdb --database graphite
python3 run_eval.py --dataset weather --lines 100000 --columns 46 --algorithm recovdb --database kairosdb-h2
python3 run_eval.py --dataset weather --lines 100000 --columns 46 --algorithm recovdb --database kairosdb-cassandra
python3 run_eval.py --dataset weather --lines 100000 --columns 46 --algorithm recovdb --database druid
```

Activity

```bash
python3 run_eval.py --dataset activity --lines 10000 --columns 360 --algorithm recovdb --database influx
python3 run_eval.py --dataset activity --lines 10000 --columns 360 --algorithm recovdb --database timescaledb
python3 run_eval.py --dataset activity --lines 10000 --columns 360 --algorithm recovdb --database monetdb
python3 run_eval.py --dataset activity --lines 10000 --columns 360 --algorithm recovdb --database extremedb
python3 run_eval.py --dataset activity --lines 10000 --columns 360 --algorithm recovdb --database graphite
python3 run_eval.py --dataset activity --lines 10000 --columns 360 --algorithm recovdb --database kairosdb-h2
python3 run_eval.py --dataset activity --lines 10000 --columns 360 --algorithm recovdb --database kairosdb-cassandra
python3 run_eval.py --dataset activity --lines 10000 --columns 360 --algorithm recovdb --database druid
```

Medical

```bash
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm recovdb --database influx
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm recovdb --database timescaledb
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm recovdb --database monetdb
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm recovdb --database extremedb
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm recovdb --database graphite
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm recovdb --database kairosdb-h2
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm recovdb --database kairosdb-cassandra
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm recovdb --database druid
```

Monitoring

```bash
python3 run_eval.py --dataset monitoring --lines 500 --columns 6000 --algorithm recovdb --database influx
python3 run_eval.py --dataset monitoring --lines 500 --columns 6000 --algorithm recovdb --database timescaledb
python3 run_eval.py --dataset monitoring --lines 500 --columns 6000 --algorithm recovdb --database monetdb
python3 run_eval.py --dataset monitoring --lines 500 --columns 6000 --algorithm recovdb --database extremedb
python3 run_eval.py --dataset monitoring --lines 500 --columns 6000 --algorithm recovdb --database graphite
python3 run_eval.py --dataset monitoring --lines 500 --columns 6000 --algorithm recovdb --database kairosdb-h2
python3 run_eval.py --dataset monitoring --lines 500 --columns 6000 --algorithm recovdb --database kairosdb-cassandra
python3 run_eval.py --dataset monitoring --lines 500 --columns 6000 --algorithm recovdb --database druid
```

##### FIGURE 4.12 Runtime of data repair algorithm (QB5) – Screen.

Weather

```bash
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm screen --database influx
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm screen --database timescaledb
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm screen --database monetdb
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm screen --database extremedb
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm screen --database graphite
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm screen --database kairosdb-h2
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm screen --database kairosdb-cassandra
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm screen --database druid
```

Activity

```bash
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm screen --database influx
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm screen --database timescaledb
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm screen --database monetdb
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm screen --database extremedb
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm screen --database graphite
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm screen --database kairosdb-h2
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm screen --database kairosdb-cassandra
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm screen --database druid
```

Medical

```bash
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm screen --database influx
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm screen --database timescaledb
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm screen --database monetdb
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm screen --database extremedb
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm screen --database graphite
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm screen --database kairosdb-h2
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm screen --database kairosdb-cassandra
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm screen --database druid
```

Monitoring

```bash
python3 run_eval.py --dataset monitoring --lines 2205 --columns 20000 --algorithm screen --database influx
python3 run_eval.py --dataset monitoring --lines 2205 --columns 20000 --algorithm screen --database timescaledb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 20000 --algorithm screen --database monetdb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 20000 --algorithm screen --database extremedb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 20000 --algorithm screen --database graphite
python3 run_eval.py --dataset monitoring --lines 2205 --columns 20000 --algorithm screen --database kairosdb-h2
python3 run_eval.py --dataset monitoring --lines 2205 --columns 20000 --algorithm screen --database kairosdb-cassandra
```

##### FIGURE 4.13 Runtime of data repair algorithm (QB6) – K-Means.

Weather

```bash
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm kmeans --database influx
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm kmeans --database timescaledb
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm kmeans --database monetdb
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm kmeans --database extremedb
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm kmeans --database graphite
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm kmeans --database kairosdb-h2
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm kmeans --database kairosdb-cassandra
python3 run_eval.py --dataset weather --lines 1000000 --columns 46 --algorithm kmeans --database druid
```

Activity

```bash
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm kmeans --database influx
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm kmeans --database timescaledb
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm kmeans --database monetdb
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm kmeans --database extremedb
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm kmeans --database graphite
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm kmeans --database kairosdb-h2
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm kmeans --database kairosdb-cassandra
python3 run_eval.py --dataset activity --lines 100000 --columns 360 --algorithm kmeans --database druid
```

Medical

```bash
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm kmeans --database influx
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm kmeans --database timescaledb
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm kmeans --database monetdb
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm kmeans --database extremedb
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm kmeans --database graphite
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm kmeans --database kairosdb-h2
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm kmeans --database kairosdb-cassandra
python3 run_eval.py --dataset medical --lines 7000 --columns 512 --algorithm kmeans --database druid
```

Monitoring

```bash
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm kmeans --database influx
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm kmeans --database timescaledb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm kmeans --database monetdb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm kmeans --database extremedb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm kmeans --database graphite
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm kmeans --database kairosdb-h2
python3 run_eval.py --dataset monitoring --lines 2205 --columns 40000 --algorithm kmeans --database kairosdb-cassandra
```

##### FIGURE 4.14 Runtime  of KNN (QB7).

Weather

```bash
python3 run_eval.py --dataset weather --lines 5000 --columns 46 --algorithm knn --database influx
python3 run_eval.py --dataset weather --lines 5000 --columns 46 --algorithm knn --database timescaledb
python3 run_eval.py --dataset weather --lines 5000 --columns 46 --algorithm knn --database monetdb
python3 run_eval.py --dataset weather --lines 5000 --columns 46 --algorithm knn --database extremedb
python3 run_eval.py --dataset weather --lines 5000 --columns 46 --algorithm knn --database graphite
python3 run_eval.py --dataset weather --lines 5000 --columns 46 --algorithm knn --database kairosdb-h2
python3 run_eval.py --dataset weather --lines 5000 --columns 46 --algorithm knn --database kairosdb-cassandra
python3 run_eval.py --dataset weather --lines 5000 --columns 46 --algorithm knn --database druid
```

Activity

```bash
python3 run_eval.py --dataset activity --lines 5000 --columns 360 --algorithm knn --database influx
python3 run_eval.py --dataset activity --lines 5000 --columns 360 --algorithm knn --database timescaledb
python3 run_eval.py --dataset activity --lines 5000 --columns 360 --algorithm knn --database monetdb
python3 run_eval.py --dataset activity --lines 5000 --columns 360 --algorithm knn --database extremedb
python3 run_eval.py --dataset activity --lines 5000 --columns 360 --algorithm knn --database graphite
python3 run_eval.py --dataset activity --lines 5000 --columns 360 --algorithm knn --database kairosdb-h2
python3 run_eval.py --dataset activity --lines 5000 --columns 360 --algorithm knn --database kairosdb-cassandra
python3 run_eval.py --dataset activity --lines 5000 --columns 360 --algorithm knn --database druid
```

Medical

```bash
python3 run_eval.py --dataset medical --lines 3500 --columns 512 --algorithm knn --database influx
python3 run_eval.py --dataset medical --lines 3500 --columns 512 --algorithm knn --database timescaledb
python3 run_eval.py --dataset medical --lines 3500 --columns 512 --algorithm knn --database monetdb
python3 run_eval.py --dataset medical --lines 3500 --columns 512 --algorithm knn --database extremedb
python3 run_eval.py --dataset medical --lines 3500 --columns 512 --algorithm knn --database graphite
python3 run_eval.py --dataset medical --lines 3500 --columns 512 --algorithm knn --database kairosdb-h2
python3 run_eval.py --dataset medical --lines 3500 --columns 512 --algorithm knn --database kairosdb-cassandra
python3 run_eval.py --dataset medical --lines 3500 --columns 512 --algorithm knn --database druid
```

Monitoring

```bash
python3 run_eval.py --dataset monitoring --lines 1000 --columns 20000 --algorithm knn --database influx
python3 run_eval.py --dataset monitoring --lines 1000 --columns 20000 --algorithm knn --database timescaledb
python3 run_eval.py --dataset monitoring --lines 1000 --columns 20000 --algorithm knn --database monetdb
python3 run_eval.py --dataset monitoring --lines 1000 --columns 20000 --algorithm knn --database extremedb
python3 run_eval.py --dataset monitoring --lines 1000 --columns 20000 --algorithm knn --database graphite
python3 run_eval.py --dataset monitoring --lines 1000 --columns 20000 --algorithm knn --database kairosdb-h2
python3 run_eval.py --dataset monitoring --lines 1000 --columns 20000 --algorithm knn --database kairosdb-cassandra
```

##### FIGURE 4.15: Runtime of KNN (QB7) using database operators

```bash
python3 run_eval.py --dataset weather --lines 10000 --columns 46 --algorithm knn-operators --database timescaledb
python3 run_eval.py --dataset weather --lines 10000 --columns 46 --algorithm knn-operators --database monetdb
python3 run_eval.py --dataset weather --lines 10000 --columns 46 --algorithm knn-operators --database extremedb
```

##### FIGURE 4.16: Runtime of Anomalies detection (QB8)

Weather

```bash
python3 run_eval.py --dataset weather --lines 2000 --columns 46 --algorithm hotsax --database influx
python3 run_eval.py --dataset weather --lines 2000 --columns 46 --algorithm hotsax --database timescaledb
python3 run_eval.py --dataset weather --lines 2000 --columns 46 --algorithm hotsax --database monetdb
python3 run_eval.py --dataset weather --lines 2000 --columns 46 --algorithm hotsax --database extremedb
python3 run_eval.py --dataset weather --lines 2000 --columns 46 --algorithm hotsax --database graphite
python3 run_eval.py --dataset weather --lines 2000 --columns 46 --algorithm hotsax --database kairosdb-h2
python3 run_eval.py --dataset weather --lines 2000 --columns 46 --algorithm hotsax --database kairosdb-cassandra
python3 run_eval.py --dataset weather --lines 2000 --columns 46 --algorithm hotsax --database druid
```

Activity

```bash
python3 run_eval.py --dataset activity --lines 1000 --columns 360 --algorithm hotsax --database influx
python3 run_eval.py --dataset activity --lines 1000 --columns 360 --algorithm hotsax --database timescaledb
python3 run_eval.py --dataset activity --lines 1000 --columns 360 --algorithm hotsax --database monetdb
python3 run_eval.py --dataset activity --lines 1000 --columns 360 --algorithm hotsax --database extremedb
python3 run_eval.py --dataset activity --lines 1000 --columns 360 --algorithm hotsax --database graphite
python3 run_eval.py --dataset activity --lines 1000 --columns 360 --algorithm hotsax --database kairosdb-h2
python3 run_eval.py --dataset activity --lines 1000 --columns 360 --algorithm hotsax --database kairosdb-cassandra
python3 run_eval.py --dataset activity --lines 1000 --columns 360 --algorithm hotsax --database druid
```

Medical

```bash
python3 run_eval.py --dataset medical --lines 700 --columns 512 --algorithm hotsax --database influx
python3 run_eval.py --dataset medical --lines 700 --columns 512 --algorithm hotsax --database timescaledb
python3 run_eval.py --dataset medical --lines 700 --columns 512 --algorithm hotsax --database monetdb
python3 run_eval.py --dataset medical --lines 700 --columns 512 --algorithm hotsax --database extremedb
python3 run_eval.py --dataset medical --lines 700 --columns 512 --algorithm hotsax --database graphite
python3 run_eval.py --dataset medical --lines 700 --columns 512 --algorithm hotsax --database kairosdb-h2
python3 run_eval.py --dataset medical --lines 700 --columns 512 --algorithm hotsax --database kairosdb-cassandra
python3 run_eval.py --dataset medical --lines 700 --columns 512 --algorithm hotsax --database druid
```

Monitoring

```bash
python3 run_eval.py --dataset monitoring --lines 500 --columns 700 --algorithm hotsax --database influx
python3 run_eval.py --dataset monitoring --lines 500 --columns 700 --algorithm hotsax --database timescaledb
python3 run_eval.py --dataset monitoring --lines 500 --columns 700 --algorithm hotsax --database monetdb
python3 run_eval.py --dataset monitoring --lines 500 --columns 700 --algorithm hotsax --database extremedb
python3 run_eval.py --dataset monitoring --lines 500 --columns 700 --algorithm hotsax --database graphite
python3 run_eval.py --dataset monitoring --lines 500 --columns 700 --algorithm hotsax --database kairosdb-h2
python3 run_eval.py --dataset monitoring --lines 500 --columns 700 --algorithm hotsax --database kairosdb-cassandra
```

##### FIGURE 4.17: Runtime of Similiarity search (QB9)

Monitoring

```bash
python3 run_eval.py --dataset monitoring --lines 2205 --columns 5000 --algorithm hotsax --database influx
python3 run_eval.py --dataset monitoring --lines 2205 --columns 5000 --algorithm hotsax --database timescaledb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 5000 --algorithm hotsax --database monetdb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 5000 --algorithm hotsax --database extremedb
python3 run_eval.py --dataset monitoring --lines 2205 --columns 5000 --algorithm hotsax --database graphite
python3 run_eval.py --dataset monitoring --lines 2205 --columns 5000 --algorithm hotsax --database kairosdb-h2
python3 run_eval.py --dataset monitoring --lines 2205 --columns 5000 --algorithm hotsax --database kairosdb-cassandra
python3 run_eval.py --dataset monitoring --lines 2205 --columns 5000 --algorithm hotsax --database druid
```

___
## Running eval

Each of the databases has a dedicated directory in Databases. In them, there is a dedicated directory for each experiment. In order to run an experiment, go to the directory of the experiment and use the Python3 script there. For example,

```bash
$ cd Databases/influx/kmeans
$ python3 generate_udf.py
```

Note that the scripts can be configured to run on different datasets and different dimensions. For example,
```bash
$ cd Databases/influx/kmeans
$ python3 generate_udf.py --file <path_to_file> --lines 1000 --columns 50
```
