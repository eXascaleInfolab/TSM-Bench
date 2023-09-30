 # Comprehensive Benchmark for Time Series Database Systems

TSM-Bench is a new benchmark that compares seven Time Series Database Systems (TSDBs) using a mixed set of workloads. It can be easily extended with new systems, queries, datasets, and workloads. The benchmark introduces a novel data generation method that augments seed real-world time series datasets enabling realistic and scalable benchmarking. Technical details can be found in the paper: [TSM-Bench: Benchmarking Time Series Database Systems for Monitoring Applications](https://www.vldb.org/pvldb/vol16/p3363-khelifati.pdf), PVLDB'23. 

- List of benchmarked systems: [ClickHouse](https://clickhouse.com/), [Druid](https://druid.apache.org/), [eXtremeDB](https://www.mcobject.com/)*, [InfluxDB](https://docs.influxdata.com/influxdb/v1.7/), [MonetDB](https://www.monetdb.org/easy-setup/), [QuestDB](https://questdb.io/), [TimescaleDB](https://www.timescale.com/).
-  The benchmark evaluates bulk-loading, storage performance, and offline/online query performance. 
- We use two datasets for the evaluation: *D-LONG [d1] and D-MULTI [d2]*. The evaluated datasets can be found [here](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/datasets).
- <sup>*</sup>**Note**: Due to license restrictions, we can only share the evaluation version of extremeDB. The results between the benchmarked and the public version might diverge. 

[**Prerequisites**](#prerequisites) | [**Build Datasets**](#build-datasets) | [**Installation**](#systems-setup) | [**Experiments**](#experiments) | [**Data Generation**](#data-generation) | [**Benchmark Extension**](#benchmark-extension) | [**Technical Report**](#technical-report) | [**Contributors**](#contributors)




___
## Prerequisites

- Ubuntu 20 (including Ubuntu derivatives, e.g., Xubuntu); 128 GB RAM
- Clone this repository

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

## Datasets Building & Loading 

- Download and decompress Dataset 1 (takes ~ 10 mins)

```bash
cd datasets
sh build.sh d1
cd ..

```

- Load Dataset 1 into all the systems (takes ~ 2 hours)
  
```bash
cd systems
sh load_all.sh d1
cd ..
```

- **Note**: To build and load the larger dataset d2, replace ```d1``` with ```d2```.

 <!---  
-  To download, install, setup and load dataset ```d1``` to systems

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



### Storage Performance 

- To compute the storage performance for a given system: 
    ```bash
    cd systems/{system}
    sh compression.sh
    ```
- Note: {system} needs to be replaced with the name of one of the systems from the table below.

### Offline Workload

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
| all  | q8 (distance based similarity search) | |
|  | q9 (DTW) | |
|  | all | |


- **Optional Arguments**: The following arguments allow to add variation in the number of sensors and dynamic changes in predicate ranges:
    - `--nb_st`: Number of queried stations when varying other dimensions (Default = 1)
    - `--nb_sr`: Number of queried sensors when varying other dimensions (Default = 3)
    - `--range`: Query range value when varying other dimensions (Default = 1)
    - `--rangeUnit`: Query range unit when varying other dimensions (Default = day)
    - `--timeout`: Maximum query time after 5 runs (s) (Default = 20)
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


This workload requires two servers: the first one serves as a host machine to deploy the systems (similar to above) and the second one runs as a client to generate writes and queries.

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
2. Execute the online query on the client side using the --host flag (see examples below).
   
3. Stop the system on the host server
   ```bash
   sh stop.sh
   ```   

**Optional Arguments**:
- `--host` : remote host machine name (Default = "localhost")
- `--n_threads` : Number of threads to use. (Default 10)
- `--batch_start`: Number data points to be inserted each second (if possible) in each thread (Default = 10000)
- `--batch_step`: Number data points to be inserted each second (if possible) in each thread (Default = 10000)


  
**Examples**:

1. Run query q1 in an online manner on clickhouse.

```bash 
python3 tsm_eval_online.py --system clickhouse --queries q1 --host "host_address"
```
2. Run all queries in an online manner on questdb using one thread.  

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


___

## Benchmark Extension

TSM-Bench allows to integrate new systems in a seamless way. We provide a step-by-step [tutorial](https://github.com/eXascaleInfolab/TSM-Bench/blob/main/systems/integration/) on how 
to integrate your system as part of the benchmark. 

___



## Time Series Generation 

We provide a [GAN-based generation](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/generation) that allows to augment a seed dataset with more and/or longer time series that
have akin properties to the seed ones. The tool can be used either directly using a pre-trained model
or by retraining from scratch the model.

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
@inproceedings{khelifati2023vldb,
  author = {Khelifati, Abdelouahab and Khayati, Mourad and Dignös, Anton and Difallah, Djellel and Cudré-Mauroux, Philippe},
  title = {TSM-Bench: Benchmarking Time Series Database Systems for Monitoring Applications},
  booktitle = {Proceedings of the VLDB Endowment},
  volume = {16},
  number = {11},
  pages = {3363--3376},
  year = {2023},
  doi = {10.14778/3611479.3611532},
  url = {https://vldb.org/2023/?papers-research}
}
```


