 # Comprehensive Benchmark for Time Series Database Systems

TSM-Bench is a new benchmark that compares seven Time Series Database Systems (TSDBs) using a mixed set of workloads. It can be easily extended with new systems, queries, datasets, and workloads. The benchmark introduces a novel data generation method that augments seed real-world time series datasets enabling realistic and scalable benchmarking. Technical details can be found in the paper: [TSM-Bench: Benchmarking Time Series Database Systems for Monitoring Applications](https://www.vldb.org/pvldb/vol16/p3363-khelifati.pdf), PVLDB'23. 

- List of benchmarked systems: [ClickHouse](https://clickhouse.com/), [Druid](https://druid.apache.org/), [eXtremeDB](https://www.mcobject.com/)*, [InfluxDB](https://docs.influxdata.com/influxdb/v1.7/), [MonetDB](https://www.monetdb.org/easy-setup/), [QuestDB](https://questdb.io/), [TimescaleDB](https://www.timescale.com/).
-  The benchmark evaluates bulk-loading, storage performance, and offline/online query performance. 
- We use two datasets for the evaluation: *D-LONG [d1] and D-MULTI [d2]*. The evaluated datasets can be found [here](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/datasets).
- <sup>*</sup>**Note**: Due to license restrictions, we can only share the evaluation version of extremeDB. The results between the benchmarked and the public version might diverge. 

<!---
  , in addition to additional generation scripts used during the online workloads.

-->

[**Prerequisites**](#prerequisites) | [**Build Datasets**](#build-datasets) | [**Installation**](#systems-setup) | [**Experiments**](#experiments) | [**Data Generation**](#data-generation) | [**System Integration**](#system-integration) | [**Technical Report**](#technical-report)

<!---
| Dataset | # of TS | # of Stations | # of Sensors per station | Length of TS | Time Period | 
| ------ | ------ | ------ | ------ | ------ | ------ |
| d1 | 1K | 10 | 100 | 5.18M | 01-03-2019 to 30-04-2019 | 
| d2 | 200K | 2000 | 100 | 17.2B | 01-02-2019 to 10-02-2019 | 


- [**New**] : [TSM_Technical_Report](https://github.com/eXascaleInfolab/TSM-Bench/blob/main/results/TSM_Technical_Report.pdf) which contains additional experiments on
    - Advanced queries in SQL and UDF.
    - Impact of data characteristics.
-->


___
## Prerequisites

- Ubuntu 20 (including Ubuntu derivatives, e.g., Xubuntu); 128 GB RAM
- Clone this repository
- Install the dependencies and activate the created virtual environment 
  
    ```bash
    sh systems/install_dependencies.sh
    source TSMvenv/bin/activate
    ```
___


## Build Datasets 

Building a dataset consists of downloading and decompressing it, making it ready to be loaded into the DB. The benchmark can be run using 
Dataset 1, Dataset 2, or both.

- Build Dataset 1 (takes ~ 10 mins)

    ```bash
    cd datasets/
    sh build_d1.sh
    cd ..
    ```

- Build Dataset 2 (takes ~ 2 hours on a 1GBps network; requires at least 300GB of disk space)

    ```bash
    cd datasets/
    sh build_d2.sh
    cd ..
    ```

___
## Systems Setup

- To install and load dataset d1 into  clickhouse, extremedb, monetdb, questdb, and timescaledb  (takes ~40mins)

```bash
cd systems/
sh install_all.sh
```

- We recommend to install influxdb and druid separately. To install the two systems and load d1, run the following commands---after installing each system, user input is required (takes ~50mins)

```bash
cd ../influxdb
sh install.sh
```

```bash
cd systems/druid
sh install.sh
```


- **Note**: To load the larger dataset d2, uncomment the respective lines in ```load.sh``` in each system folder.


<!---

### Data Loading

To load Dataset 1 into the systems

```bash
cd ../
sh load_all.sh
```
-->




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

### Query Execution (Offline)

- Each system has a dedicated subfolder under `systems` folder. Queries for all systems can be executed as follows:

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

### Query Execution (Online)


This workload requires two servers: the first to deploy the systems (similar as above) and the second runs as a client to generate writes and queries.
To configure the second server: 
1. Clone this repo
2. Install dependencies:

    ```bash
    sh systems/install_dependencies.sh
    ```
3. Install the systems client libraries
   
    ```bash
    sh systems/independent_system_install.sh
    ```
4. Run the system on the host server (server 1)

   ```bash
   cd systems/{system}
   sh launch.sh
   ```   
5. Execute the online query using the --host flag.
   
6. Stop the system on the host server
   ```bash
   sh stop.sh
   ```   

**Optional Arguments**:
- `--host` : remote host machine name (Default = "localhost")
- `--n_threads` : Number of threads to use. (Default 10)
- `--batch_start`: Number data points to be inserted each second (if possible) in each thread (Default = 100)
- `--batch_step`: Number data points to be inserted each second (if possible) in each thread (Default = 100)

**Notes**:

- We launch each system separately on the local machine and execute the online query on a remote machine using the --host flag.
- The targeted ingestion  rate per second equals to batchsize*n_threads*100.
- The maximal batchsize depends on your architecture and selected system.
- Druid supports ingestion and queries concurrently, while QuestDB and MonetDB do not support multithreading.
- If you stop the program before its termination or shut down the system, the database might not be set into its initial state properly; you need to reload the dataset in the host machine:
    ```bash
   cd systems/{system}
   sh load.sh
   ```   
  
  
**Examples**:

```bash 
python3 tsm_eval_online.py --systems clickhouse --queries q1 --host "your_server_name"
```

```bash 
python3 tsm_eval_online.py --systems questdb --queries all --n_threads 1 --host "your_server_name" 
```
___

- **Results**: All the runtimes and plots will be added to the `results` folder in the second server.
    - The runtime results of the systems will be added to: `results/online/{dataset}/{query}/runtime/`. The runtime plots will be added to the folder `results/online/{dataset}/{query}/plots/`.
   
    - All the queries return the runtimes by varying the ingestion rate.

## Time Series Generation 

We provide a GAN-based generation that allows to augment a seed dataset with more and/or longer time series that
have akin properties to the seed ones. The tool can be used either directly using a pre-trained model
or by retraining from scratch the model.

### Install Requirements

```bash
cd generation
install.sh
```

### Execution using a Pre-trained Model 

```bash
python3 run_pretrained.py
```
The generated plots and data are stored in the `generation/results` folder.

### Execution using Model Training

#### Model Training

- **Step 1:** Train a GAN model on data segments located in `data/` and write the resulting segments into `generation/` (takes ~3 days) 

```bash
python3 DCGAN.py
python3 encoder_dc.py
```

- **Step 2:** Generate new segments using the trained ones from Step 1 (takes ~46 seconds)

```bash
python3 test_dc.py
```
#### Data Generation

- **Step 3:** Apply LSH to generate long time series (takes ~20 seconds)

```bash
python3 gen_ts.py
```
### Sample Generation Plots:

![image](https://github.com/eXascaleInfolab/TSM-Bench/assets/15266242/13d8c2f9-fdbf-495f-aaf9-7f5ec0999470)

___
## System Integration

TBA

___

## Technical Report

Additional results not reported in the paper can be found [here](https://github.com/eXascaleInfolab/TSM-Bench/blob/main/TSM_Technical_Report.pdf). The additional experiments cover: 

- Advanced analytical queries in SQL and UDF
- Selection of the evaluated systems
- Parameterization of the systems
- Impact of data characteristics

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


