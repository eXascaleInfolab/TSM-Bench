# TSM-Bench: Benchmarking Time Series Database Systems for Monitoring Applications

TSM-Bench implements seven Time Series Database Systems (TSDBs) for a mixture set of worklods. The benchmark can be easily extended with new systems, queries, datasets, and workloads. The benchmark proposes a novel data generation method that augments seed real-world time series datasets enabling realistic and scalable benchmarking. This benchmark is a paper under review for VLDB 2023. 

- The benchmark implements the following TSDBs: [ClickHouse](https://clickhouse.com/), [Druid](https://druid.apache.org/), [eXtremeDB](https://www.mcobject.com/), [InfluxDB](https://docs.influxdata.com/influxdb/v1.7/), [MonetDB](https://www.monetdb.org/easy-setup/), [QuestDB](https://questdb.io/), [TimescaleDB](https://www.timescale.com/).
- This benchmark evaluates bulk-loading, storage performance, and query performance in both offline and online of TSDBs. 
- The evaluated **datasets** can be found [here](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/datasets). The datasets include the two datasets *D-LONG[d1], D-MULTI[d2]*, in addition to additional generation scripts that are used during the online workloads. 
- **Additional experiments and results**  can be found [here](https://github.com/eXascaleInfolab/TSM-Bench/blob/main/results/TSM_Bench%5BAdditional_results%5D.pdf).
- **User-Defined Functions (UDFs)** codes and examples to run can be found [here](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/udfs). Results could be found [here](https://github.com/eXascaleInfolab/TSM-Bench/blob/main/results/TSM_Bench%5BAdditional_results%5D.pdf).

___
[**Prerequisites and dependencies**](#prerequisites) | [**Datasets**](#datasets) | [**Systems installation and configuration**](#systems-installation-and-configuration) | [**Data Loading**](#data-loading) | [**Storage Performance**](#storage-performance) | [**Query Execution**](#query-execution) | [**Arguments**](#arguments) | [**Examples**](#examples)

___
## Prerequisites

- Ubuntu 18 or higher
- Clone this repository
- All other dependencies will be installed via the install script


- Install all dependencies (~ 3 mins)

	```bash
	cd systems
	sh install_dependencies.sh
	```

___
## Datasets 

The dimensions of the two datasets used in this benchmark are the following:

| Dataset | # of TS | # of Stations | # of Sensors per station | Length of TS | Time Period | 
| ------ | ------ | ------ | ------ | ------ | ------ |
| d1 | 1K | 10 | 100 | 5.18M | 01-03-2019 to 30-04-2019 | 
| d2 | 200K | 2000 | 100 | 17.2B | 01-02-2019 to 10-02-2019 | 

#### Build Datasets 

Building a dataset consists of downloading it and decompressing it, making it ready to be loaded into the TSDBs

- Build Dataset 1 (~ 11 mins)

	```bash
	cd ../datasets/
	sh install_d1.sh
	```

- Build Dataset 2 Make sure you have at least free 300GB of free disk space to install this dataset (~ 2 hours on a 1GBps network)

	```bash
	cd ../datasets/
	sh install_d2.sh
	```

___
## Systems installation and configuration

- Download and install all systems

	```bash
	cd systems
	sh install_all.sh
	```
- Setup all systems (all systems have to be running) to have two datasets ```d1``` and ```d2```

	```bash
	cd systems
	sh setup_all.sh
	```
___
##  Data Loading 

- **[Table 3: Loading Performance]** Evaluate data loading to all systems (all systems have to be running), the results will be printed after the loading is done for each system

	```bash
	cd systems
	sh load_all.sh
	```

___
## Storage Performance 

- **[Table 3: Storage Performance]** The storage performance of a system could be accessed as follows 
	```bash
	cd systems/{system}
	sh compression.sh
	```

___
## Query Execution [Query, Vary & Plot]

- Each of the systems has a dedicated subfolder under `systems` folder. Queries for all systems could be queried as followed from the main directory

	```bash
	python3 run_eval.py [args]
	```

The scripts would connect to the systems, run all the queries varying the parameters, obtain the results and plot them

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
|  | q8 (distance based similarity search) | |
|  | q9 (DTW) | |


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

1. **[Figure 3.a]** Run query q1 on InfluxDB for Dataset 1 with the default parameters (range=1 day, n_st=1, n_s=3)
 
```bash 
python3 run_eval.py --systems influx --datasets d1 --queries "q1"
```

2. **[Figure 4]** Run queries q3 and q4 on InfluxDB for Dataset 1 with the default parameters (range=1 day, n_st=1, n_s=3)
 
```bash 
python3 run_eval.py --systems influx --datasets d1 --queries "q3 q4"
```

3. **[Figures 3-5]** Run all queries on InfluxDB on Dataset 1 with the default parameters
 
```bash 
python3 run_eval.py --systems influx --datasets d1
```

4. **[Figure 5]** Run q5 on InfluxDB on Dataset 1 with the default parameters with a 1 minute timeout per query type
 
```bash 
python3 run_eval.py --systems influx --datasets d1  --queries "q5" --timeout 60
```

5. **[Figure 6]** Run all queries on InfluxDB on Dataset 2 with the default parameters while varying the number of stations
 
```bash 
python3 run_eval.py --systems influx --datasets d1 --rangeUnit day --def_s 3 
```

6. Run query q1 on InfluxDB with custom parameters (range=1 week, n_st=100, n_s=3)
 
```bash 
python3 run_eval.py --systems influx --datasets d1 --queries q1 --def_st 100 --def_s 3 --range 1 --rangeUnit day

```
