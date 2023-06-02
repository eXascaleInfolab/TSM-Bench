# TSM-Bench: Benchmarking Time Series Database Systems for Monitoring Applications

TSM-Bench implements seven Time Series Database Systems (TSDBs) for a mixture set of worklods. The benchmark can be easily extended with new systems, queries, datasets, and workloads. The benchmark proposes a novel data generation method that augments seed real-world time series datasets enabling realistic and scalable benchmarking. 

- The benchmark implements the following TSDBs: [ClickHouse](https://clickhouse.com/), [Druid](https://druid.apache.org/), [eXtremeDB](https://www.mcobject.com/), [InfluxDB](https://docs.influxdata.com/influxdb/v1.7/), [MonetDB](https://www.monetdb.org/easy-setup/), [QuestDB](https://questdb.io/), [TimescaleDB](https://www.timescale.com/).
- This benchmark evaluates bulk-loading, query performance in both offline and online, and storage performance of TSDBs. 
- The full list of evaluated **datasets** can be found [here](). The datasets include the two datasets *D-LONG, D-MULTI*, in addition to additional generation scripts that are used during the online workloads. 
- The **results** of our benchmark can be found [here]().
- **Additional experiments** and their results can be found [here]().
- User-Defined Functions (**UDFs**) codes, experiments and results can be found [here]().

___
[**Prerequisites and dependencies**](#prerequisites) | [**Datasets**](#datasets) | [**Build**](#build) | [**Query Execution**](#Query-Execution) | [**Storage Performance**](#Storage-Performance) | [**Arguments**](#arguments) | [**Examples**](#examples)

___
## Prerequisites and dependencies

- Ubuntu 18 or higher
- Clone this repository
- All other dependencies will be installed via the install script.


## Datasets 

The dimensions of the two datasets used in this benchmark are the following:

| Dataset | # of TS | # of Stations | # of Sensors per station | Length of TS | 
| ------ | ------ | ------ | ------ | ------ |
| d1 | 1K | 10 | 100 | 5.18M |
| d2 | 200K | 2000 | 100 | 17.2B |

___
## Build

- Install all dependencies (~ 3 mins)

```bash
cd systems
sh install_dependencies.sh
```

- Build Dataset 1 (~ 11 mins)

```bash
cd ../datasets/
sh install_d1.sh
```

- Build Dataset 2 Make sure you have at least free 300GB of free disk space to install this dataset (~ 2 hours on a 1GBps network). 

```bash
cd ../datasets/
sh install_d2.sh
```


- Download and install all systems

```bash
cd systems
sh install_all.sh
```

To build a particular database, run the installation script located in the database folder. For example, to install clickhouse

```bash
cd database/clickhouse
sh install.sh
```

___
## Storage Performance

The storage performance of a system could be accessed as follows: 

```bash
    $ cd systems/{system}
    $ sh compression.sh
```

___
## Query Execution

Each of the systems has a dedicated subfolder under `systems` folder. Queries for all systems could be queried as followed from the main directory. 

```bash
	$ python3 run_eval.py [args]
```

### Arguments 
| --system | --queries | --datasets |
| ------ | ------ | ------ |
| clickhouse | q1 (selection) | d1 |
| druid | q2 (filtering) | d2 |
| extremedb | q3 (aggregation) |  |
| influx | q4 (downsampling) |  |
| monetdb | q5 (upsampling) |  |
| questdb | q6 (average) | |
| timescaledb | q7 (correlation) | |


### Optional arguments

 | args  |  Interpretation | Default value | 
 | --------    | ------- | ------- | 
 | --nb_st   |  Number of stations in the dataset | 10
 | --nb_s   |  Number of sensors in a station | 100
 | --def_st   |   Number of queried stations | 1
 | --def_s   |   Number of queried sensors | 3
 | --rangeUnit   |  Query range unit | day
 | --min_ts   |   Minimum query timestamp | "2019-04-01T00:00:00" |
 | --max_ts   |   Maximum query timestamp | "2019-04-30T00:00:00"
 | --timeout   |   Maximum query time after 5 runs (s) | 20



### Examples

1. Run queries q1 and q4 on InfluxDB for Dataset 1 with the default parameters (range=1 day, n_st=1, n_s=3)
 
```bash 
python3 run_eval.py --systems influx --datasets d1 --queries "q1 q4"
```

2. Run query q1 on InfluxDB with custom parameters (range=1 week, n_st=100, n_s=3)
 
```bash 
python3 run_eval.py --systems influx --datasets d1 --queries q1 --def_st 100 --def_s 3 --range 1 --rangeUnit day

```

3. Run all queries on InfluxDB on Dataset 1 with the default parameters
 
```bash 
python3 run_eval.py --systems influx --datasets d1
```

4. Run all queries on InfluxDB on Dataset 1 with the default parameters with a 1 minute timeout per query type
 
```bash 
python3 run_eval.py --systems influx --datasets d1 --timeout 60
```


