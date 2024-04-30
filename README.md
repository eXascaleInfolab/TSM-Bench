 # Comprehensive Benchmark for Time Series Database Systems

TSM-Bench is a new benchmark that compares seven Time Series Database Systems (TSDBs) using a mixed set of workloads. It can be easily extended with new systems, queries, datasets, and workloads. The benchmark introduces a novel data generation method that augments seed real-world time series datasets, enabling realistic and scalable benchmarking. Technical details can be found in the paper [TSM-Bench: Benchmarking Time Series Database Systems for Monitoring Applications](https://www.vldb.org/pvldb/vol16/p3363-khelifati.pdf), PVLDB'23. 

- List of benchmarked systems: [ClickHouse](https://clickhouse.com/), [Druid](https://druid.apache.org/), [eXtremeDB](https://www.mcobject.com/)*, [InfluxDB](https://docs.influxdata.com/influxdb/v1.7/), [MonetDB](https://www.monetdb.org/easy-setup/), [QuestDB](https://questdb.io/), [TimescaleDB](https://www.timescale.com/).
- The benchmark evaluates bulk-loading,  storage performance, offline/online query performance, and the impact of time series features on compression.
- We use two datasets for the evaluation: *D-LONG [d1] and D-MULTI [d2]*. The evaluated datasets can be found [here](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/datasets).
- <sup>*</sup>**Note**: Due to license restrictions, we can only share the evaluation version of extremeDB. The results between the benchmarked and the public version might diverge. 

[**Prerequisites**](#prerequisites) | [**Installation**](#systems-setup) | [**Datasets Loading**](#datasets-loading) | [**Experiments**](#experiments) | [**Benchmark Extension**](#benchmark-extension) | [**Technical Report**](#technical-report) | [**Data Generation**](#time-series-generation) | [**Contributors**](#contributors)


___
## Prerequisites

- Ubuntu 22 (including Ubuntu derivatives, e.g., Xubuntu); 128 GB RAM
- Clone this repository (this can take a couple of minutes as it uploads one of the datasets)

___



## Systems Setup

- Install the dependencies and activate the created virtual environment 
  
```bash
cd systems/
sh install_dep.sh
source TSMvenv/bin/activate
```

- Install all the systems (takes ~15mins)

```bash
sh install_all_sys.sh
```

## Datasets Loading 

- Download and decompress Dataset 1 (takes ~ 3 mins)

```bash
cd ../datasets
sh build.sh d1

```

- Load Dataset 1 into all the systems (takes ~ 2 hours)
  
```bash
sh load_all.sh d1
```

- **Note**: To build and load the larger dataset d2, replace ```d1``` with ```d2```.

 <!---  
-  To download, install, setup, and load dataset ```d1``` to systems

    ```bash
    cd systems/
    sh install_all.sh
    ```
    -  Note: Systems can be installed separately as described in the [**customized installation**](#customized-installation) below. 
 

- Setup all systems (all systems have to be running) to have two datasets ```d1``` and ```d2```

    ```bash
    sh setup_all.sh
    ```

-->
___

## Experiments

 <!---  
 ###  Data Loading Performance

- To compute the data loading times of all systems (column 1 of Table 3):

    ```bash
    cd systems
    sh load_all.sh
    ```
- Note:  All systems need to be running before executing the query.  

-->

### Offline Workload
- Activate the virtual environment, if not already done:
  
   ```bash
   source systems/TSMvenv/bin/activate
   ```
   
- The offline queries for all systems can be executed from the root folder using:
   
    ```bash
    python3 tsm_eval.py [args]
    ```

- **Mandatory Arguments**: [args] should be replaced with the name of the system, query, and dataset:  


| --system | --queries | --datasets |
| ------ | ------ | ------ |
| clickhouse | q1 (selection) | d1 |
| druid | q2 (filtering) | d2 |
| extremedb* | q3 (aggregation) |  |
| influx | q4 (downsampling) |  |
| monetdb | q5 (upsampling) |  |
| questdb | q6 (average) | |
| timescaledb | q7 (correlation) | |
| all  | all | all |



- **Optional Arguments**: The following arguments allow to add variation in the number of sensors and dynamic changes in predicate ranges:
    - `--nb_st`: Number of queried stations when varying other dimensions (Default = 1)
    - `--nb_sr`: Number of queried sensors when varying other dimensions (Default = 3)
    - `--n_st`: Number of stations in the dataset (Default = 10)
    - `--n_s`: Number of sensors in the dataset (Default = 100)
    - `--nb_sr`: Number of queried sensors when varying other dimensions (Default = 3)
    - `--range`: Query range value when varying other dimensions (Default = 1)
    - `--rangeUnit`: Query range unit when varying other dimensions (Default = day)
    - `--timeout`: Maximum query time after five runs (s) (Default = 20)
    - `--min_ts`: Minimum query timestamp (Default = "2019-04-01T00:00:00")
    - `--max_ts`: Maximum query timestamp (Default = "2019-04-30T00:00:00")

- **Results**: All the runtimes and plots will be added to the `results` folder.
  
    - The runtime results of the systems for a given dataset and query will be added to: `results/offline/{dataset}/{query}/runtime/`. The runtime plots will be added to the folder `results/offline/{dataset}/{query}/plots/`.

    - All the queries return the runtimes by varying the number of stations (nb_st), number of sensors (nb_sr), and the range.

- **Examples**:

1. Run query q1 on extremedb for Dataset 1 using default parameters (nb_st=1, nb_sr=3, range=1 day)
 
```bash 
python3 tsm_eval.py --systems extremedb --queries q1 --datasets d1
```
 <!---  

2. Run query 1 on extremedb for Dataset 1 using different parameters nb_st=100, nb_sr=10, and range=1 week
 
```bash 
python3 tsm_eval.py --systems extremedb --queries q1 --datasets d1 --nb_st 10 --nb_sr 10 --range 1w
```
-->

2. Run q2 and q3 on extremedb and timescaledb for Dataset 1 
 
```bash 
python3 tsm_eval.py --systems extremedb timescaledb --queries q2 q3 --datasets d1
```

3. Run all the offline workload on all systems for Dataset 1 (takes ~ 3 hours)

```bash 
python3 tsm_eval.py --systems all --queries all --datasets d1 
```

### Online Workload


This workload requires two servers: the first serves as a host machine to deploy the systems (similar to above), and the second runs as a client to generate writes and queries.

#### Client Setup
 
- Clone this repo
- Install dependencies:

    ```bash
    cd systems/
    sh install_dep.sh
    source TSMvenv/bin/activate
    ```
- Install the system libraries
   
    ```bash
    sh install_client_lib.sh
    ```
#### Query Execution
1. Run the system on the host side 

   ```bash
   cd systems/{system}
   sh launch.sh
   ```
2. If the virtual environment is not activated from the root folder using:
  
   ```bash
   source systems/TSMvenv/bin/activate
   ```
3.  Execute the online query on the client side using the --host flag (see examples below).
   
4. Stop the system on the host server
   ```bash
   sh stop.sh
   ```   

**Optional Arguments**:
- `--host` : remote host machine name (Default = "localhost")
- `--n_threads`: Number of threads to use. (Default 10)
- `--batch_size`: Number data points to be inserted each second (if possible)  (Default = 10000)


  
**Examples**:

1. Run query q1 in an online manner on clickhouse.

```bash 
python3 tsm_eval_online.py --system clickhouse --queries q1 --host "host_address" --batch_size 10000
```

2. Run all queries online on influx using different batch sizes.
```bash 
python3 tsm_eval_online.py --system influx --queries all --host "host_address" --batch_size 10000 20000 1000000
```

3. Run all queries online on questdb using one thread.
```bash 
python3 tsm_eval_online.py --system questdb --queries all --n_threads 1 --host "host_address" 
```

**Notes**:

- We launch each system separately on the host machine and execute the online query on the client machine using the --host flag.
- The maximal batchsize depends on your architecture and the selected TSDB.
- Druid supports ingestion and queries concurrently, while QuestDB does not support multithreading.
- If you stop the program before its termination or shut down the system, the database might not be set into its initial state properly; you need to reload the dataset in the host machine:
    ```bash
   cd systems/{system}
   sh load.sh
   ```   
  

**Results**: 

- The runtime results of the systems will be added to: `results/online/{dataset}/{query}/runtime/`. 
- The runtime plots will be added to the folder `results/online/{dataset}/{query}/plots/`.
- All the queries return the runtimes by varying the ingestion rate.





### Storage Performance 

- To compute the storage performance for a given system: 
    ```bash
    cd systems/{system}
    sh compression.sh
    ```
- Note: {system} needs to be replaced with the name of one of the systems from the table below.

___

## Benchmark Extension

TSM-Bench allows the integration of new systems seamlessly. We provide a step-by-step [tutorial](https://github.com/eXascaleInfolab/TSM-Bench/blob/main/systems/integration/) on how 
to integrate your system as part of the benchmark. 

Should users wish, new queries can also be added to the benchmark. They must be added under each system's `{system}/queries.sql` file. Note that the order of the queries should be respected (e.g., q8 is the eighth query in the file).

___



## Time Series Generation 

We provide a [GAN-based generation](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/generation) that allows augmenting a seed dataset with more and/or longer time series that
have akin properties to the seed ones. The generation can be used either as a pre-trained model or by retraining from scratch the model.

___

## Technical Report

Additional results not reported in the paper can be found [here](https://github.com/eXascaleInfolab/TSM-Bench/blob/main/misc/TSM_Technical_Report.pdf). The additional experiments cover: 

- Advanced analytical queries in SQL and UDF
- Selection of the evaluated systems
- Parameterization of the systems
- Impact of data characteristics

___

## Contributors


Abdelouahab Khelifati (abdel@exascale.info), Mourad Khayati (mkhayati@exascale.info) and Luca Althaus.

___

## Citation

```bibtex
@article{DBLP:journals/pvldb/KhelifatiKDDC23,
  author       = {Abdelouahab Khelifati and
                  Mourad Khayati and
                  Anton Dign{\"{o}}s and
                  Djellel Eddine Difallah and
                  Philippe Cudr{\'{e}}{-}Mauroux},
  title        = {TSM-Bench: Benchmarking Time Series Database Systems for Monitoring
                  Applications},
  journal      = {Proc. {VLDB} Endow.},
  volume       = {16},
  number       = {11},
  pages        = {3363--3376},
  year         = {2023},
  url          = {https://www.vldb.org/pvldb/vol16/p3363-khelifati.pdf},
  doi          = {10.14778/3611479.3611532},
  timestamp    = {Mon, 23 Oct 2023 16:16:16 +0200},
  biburl       = {https://dblp.org/rec/journals/pvldb/KhelifatiKDDC23.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```


