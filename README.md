# Comprehensive Benchmark for Time Series Database Systems

TSM-Bench is a new benchmark that compares seven Time Series Database Systems (TSDBs) using a mixed set of workloads. It can be easily extended with new systems, queries, datasets, and workloads. The benchmark introduces a novel data generation method that augments seed real-world time series datasets enabling realistic and scalable benchmarking. Technical details can be found in the paper: *TSM-Bench: Benchmarking Time Series Database Systems for Monitoring Applications*, PVLDB'23. 

- List of benchmarked systems: [ClickHouse](https://clickhouse.com/), [Druid](https://druid.apache.org/), [eXtremeDB](https://www.mcobject.com/)*, [InfluxDB](https://docs.influxdata.com/influxdb/v1.7/), [MonetDB](https://www.monetdb.org/easy-setup/), [QuestDB](https://questdb.io/), [TimescaleDB](https://www.timescale.com/).
-  The benchmark evaluates bulk-loading, storage performance, and offline/online query performance. 
- We use two datasets for the evaluation: *D-LONG [d1] and D-MULTI [d2]*. The evaluated datasets can be found [here](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/datasets).
- **Note**: Due to license restrictions, we can share only the evaluation version of extremeDB. The results between the benchmarked and the public version might diverge. 

<!---
  , in addition to additional generation scripts that are used during the online workloads.

-->

[**Prerequisites**](#prerequisites) | [**Build Datasets**](#build-datasets) | [**Installation**](#systems-setup) | [**Experiments**](#experiments) | [**Data Generation**](#data-generation) | [**Technical Report**](#technical-report)

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

- Ubuntu 20.04 or higher
- Clone this repository
    ```bash
    git clone https://github.com/eXascaleInfolab/TSM-Bench 
    ```
- Install the dependencies
    ```bash
    sh systems/install_dependencies.sh
    ```
___


## Build Datasets 

Building a dataset consists of downloading and decompressing it, making it ready to be loaded into the DB

- Build Dataset 1 (takes ~ 10 mins)

    ```bash
    cd datasets/
    sh build_d1.sh
    ```

- Build Dataset 2 (takes ~ 2 hours on a 1GBps network; requires at least 300GB of disk space)

    ```bash
    cd datasets/
    sh build_d2.sh
    ```

___
## Systems Setup

We provide different scripts depending on whether the systems have been already installed or not:

   
-  To download, install, and setup all the systems

    ```bash
    cd systems/
    sh install_all.sh
    sh setup_all.sh
    ```
    -  Note: Systems can be installed separately as described in the [**customized installation**](#customized-installation) below. 
 
 - To launch the systems

   ```bash
   cd systems/
   sh launch_all.sh
   ```

    

<!---
- Setup all systems (all systems have to be running) to have two datasets ```d1``` and ```d2```

    ```bash
    sh setup_all.sh
    ```

-->
___

## Experiments
###  Data Loading Performance

- To reproduce the data loading times of all systems (column 1 of Table 3):

    ```bash
    cd systems
    sh load_all.sh
    ```
- Note:  All systems need to be running before executing the query.  

### Storage Performance 

- To reproduce the storage performance of a given system (column 2 of Table 3): 
    ```bash
    cd systems/{system}
    sh compression.sh
    ```
- Note: {system} needs to be replaced with the name of one of the systems from the table below.

### Query Execution 

- Each system has a dedicated subfolder under `systems` folder. Queries for all systems can be executed as follows:

    ```bash
    cd/
    python3 run_eval.py [args]
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
|  | q8 (distance based similarity search) | |
|  | q9 (DTW) | |

- **Optional Arguments**: The following arguments allow to add variation in the number of sensors and dynamic changes in predicate ranges:
    - `--nb_st` : Number of stations (Default = 10)
    - `--def_st` : Number of queried stations (Default = 1)
    - `--def_s` : Number of queried sensors (Default = 3)
    - `--range`: Query range value (Default = 1)
    - `--rangeUnit`: Query range unit (Default = day)
    - `--min_ts`: Minimum query timestamp (Default = "2019-04-01T00:00:00")
    - `--max_ts`: Maximum query timestamp (Default = "2019-04-30T00:00:00")
    - `--timeout` : Maximum query time after 5 runs (s) (Default = 20)

- **Examples**:

1. **[Figure 3.a]** Run query q1 on InfluxDB for Dataset 1 using default parameters (n_st=1, n_s=3, range=1 day)
 
```bash 
python3 run_eval.py --systems influx --datasets d1 --queries q1
```

2. Run q1 on InfluxDB for Dataset 1 with customized parameters (n_st=100, n_s=10, range=1 week)
 
```bash 
pythn3 run_eval.py --systems influx --datasets d1 --queries q1 --def_st 100 --def_s 10 --range 1 --rangeUnit week
```

3. **[Figures 4.a-b]** Run q3 and q4 on InfluxDB for Dataset 1 using default parameters
 
```bash 
python3 run_eval.py --systems influx --datasets d1 --queries q3 q4
```

4. **[Figures 3-4]** Run all queries on InfluxDB on Dataset 1 using default parameters
 
```bash 
python3 run_eval.py --systems influx --datasets d1
```

5. **[Figure 4.c]** Run q5 on InfluxDB on Dataset 1 with a 1-minute timeout per query type using default parameters
 
```bash 
python3 run_eval.py --systems influx --datasets d1  --queries q5 --timeout 60
```

6. **[Figure 6]** Run all queries on InfluxDB for Dataset 2 while varying the number of stations using default parameters
 
```bash 
python3 run_eval.py --systems influx --datasets d1 --rangeUnit day --def_s 3 
```





___

## Customized Installation

To install and setup a specific system

```bash
cd systems/{system}
sh install.sh
```
___

## Time Series Generation 

We provide a GAN-based generation that allows to augment a seed dataset with more and/or longer time series that
have akin properties to the seed ones. The tool can be used either directly using a pre-trained model
or by retraining from scratch the model.


### Execution using a pre-trained model 


```bash
python3 run_pretrained.py
```

### Execution using model training

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
### Sample generation plots:

![image](https://github.com/eXascaleInfolab/TSM-Bench/assets/15266242/13d8c2f9-fdbf-495f-aaf9-7f5ec0999470)

___

## Technical Report

Additional results not reported in the paper can be found [here](https://github.com/eXascaleInfolab/TSM-Bench/blob/main/TSM_Technical_Report.pdf). The additional experiments cover: 

- Advanced analytical queries in SQL and UDF
- Selection of the evaluated systems
- Parameterization of the systems
- Impact of data characteristics

___

## Citation

Coming soon



