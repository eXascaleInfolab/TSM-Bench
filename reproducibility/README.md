 # Reproducibility for TSM-Bench
 
**Paper**: Abdelouahab Khelifati, Mourad Khayati, Anton Dignös, Djellel Difallah, and Philippe Cudré-Mauroux: [TSM-Bench: Benchmarking Time Series Database Systems for Monitoring Applications](https://www.vldb.org/pvldb/vol16/p3363-khelifati.pdf). PVLDB 2023.
- **Systems**: The benchmark evaluates all the systems mentioned in the paper: TSM-Bench, [ClickHouse](https://clickhouse.com/), [Druid](https://druid.apache.org/), [eXtremeDB](https://www.mcobject.com/), [InfluxDB](https://docs.influxdata.com/influxdb/v1.7/), [MonetDB](https://www.monetdb.org/easy-setup/), [QuestDB](https://questdb.io/), [TimescaleDB](https://www.timescale.com/).
- **Datasets**: The benchmark evaluates the two datasets for the evaluation: *D-LONG [d1] and D-MULTI [d2]*. The evaluated datasets can be found [here](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/datasets).


## Prerequisites


- Ubuntu 24 (including Ubuntu derivatives, e.g., Xubuntu); 128 GB RAM; 2TB free disk space. 
- The estimated execution time for the whole reproducibility on a 32-core 6 Gbps CPU is ~7 days.

___

## Systems Setup

- Clone this repository (takes a couple of minutes as it uploads one of the datasets).

```bash
git clone https://github.com/eXascaleInfolab/TSM-Bench
```

- Install the dependencies and activate the created virtual environment (takes ~ 3 minutes)
  
```bash
cd TSM-Bench/systems/
sh install_dep.sh
source TSMvenv/bin/activate
```

- Install all the systems (takes ~ 30 minutes)

```bash
sh install_all_sys.sh
```


- Download, decompress, and load Dataset 1 (takes ~ 2 hours)

```bash
cd ../datasets
sh build.sh d1; sh load_all.sh d1
```

- Download, decompress, and load Dataset 2 (takes ~ 78 hours)

```bash
sh build.sh d2; sh load_all.sh d2
```

<!---

- Load Dataset 1 into all the systems (takes ~ 2 hours)

```bash
sh load_all.sh d1
```
-->
___
## [Table 3] Data Loading and Compression Results 

- To reproduce the results in Table 3, execute the following command:

```bash
cd ../systems
sh repro_loading.sh 
```

- The results will be written to `results` in the root folder.


___
## [Figures 3, 4, and 5] Offline Workloads D-LONG Q1-Q7 (takes ~ 7 hours)

- To reproduce the results in Figures 3, 4, and 5, execute the following command:

```bash
cd ..
python3 tsm_eval.py --systems all --queries all --datasets d1 
```
- The runtime results of the systems for each query will be added to: `results/offline/d1/{query}/runtime/`.
- The runtime plots will be added to the folder `results/offline/d1/{query}/plots/`.

___
## [Figure 6] Offline Workloads D-MULTI Q1-Q5 (takes ~ 42 hours)

- To reproduce the offline workloads D-MULTI Q1-Q5 results in Figure 6, run the following command:

```bash
python3 tsm_eval_d2.py --systems all --queries q1 q2 q3 q4 q5 --datasets d2
```

- The runtime results of the systems for each query will be added to: `results/offline/d2/{query}/runtime/`.
- The runtime plots will be added to the folder `results/offline/d2/{query}/plots/`.

___
## [Figure 7] Insertion Latency 
 
-  This experiment involves a manual configuration of the insertion rates, which is hard to automate.


___
## [Figure 9] Data Generation Performance  (takes ~ 9 hours)

- To reproduce the data generation performance results, execute the following command:

```bash
cd systems/
sh repro_generation_performance.sh 
```

- The runtimes and plots will be written to `results/generation/experiment_{i}`, where `{i}` refers to the corresponding subfigure.

___
## [Figure 10] Compression Performance (takes ~ 6 hours)

- To reproduce the compression performance results for ClickHouse, InfluxDB and TimescaleDB, run the following command. The results will be written to the `results/compression/` folder.

```bash
sh repro_characteristics.sh 
```

- To reproduce the compression performance results for Druid, follow the following [tutorial](https://github.com/eXascaleInfolab/TSM-Bench/blob/main/reproducibility/druid.md). 

___
## [Figure 8] Online Workloads D-LONG Q1-Q5 (takes ~ 7 hours)

### Requirements: 

- This experiment requires a second machine, which runs as a client, to generate writes and queries. 
- In this machine, do the following:
    - Clone this repo
    - Install the dependencies and system libraries:

  ```bash
  cd systems/
  sh install_dep.sh
  source TSMvenv/bin/activate
  sh install_client_lib.sh
  ```

### Notes

- We launch each system separately on the host machine and execute the online query on the client machine using the ```--host``` flag.
- The runtime results of the systems will be added to: `results/online/d1/{query}/runtime/`. The runtime plots will be added to the folder `results/online/d1/{query}/plots/`.
- We cannot reproduce the results of eXtremeDB, as it requires manual configuration.

### Execution

- To produce the results of **ClickHouse**
  -  Launch the system on the host machine 

   ```bash
   cd systems/clickhouse
   sh launch.sh
   ```
  - Execute the online query on the client machine, replace "host_ip" with the ip address of the server machine

   ```bash
   python3 tsm_eval_online.py --system clickhouse --queries all --host "host_ip" --batch_size 10000 20000 200000 600000 1000000 1400000
   ```

   - Stop the system on the host machine
    ```bash
   sh stop.sh
   ```

- To produce the results of **InfluxDB**
  -  Launch the system on the host machine 

   ```bash
   cd systems/influx
   sh launch.sh
   ```
  - Execute the online query on the client machine, replace "host_ip" with the ip address of the server machine

   ```bash
   python3 tsm_eval_online.py --system influx --queries all --host "host_ip" --batch_size 10000 20000 200000 600000 1000000 1400000
   ```

   - Stop the system on the host machine
    ```bash
   sh stop.sh
   ```

- To produce the results of **MonetDB**
  -  Launch the system on the host machine 

   ```bash
   cd systems/monetdb
   sh launch.sh
   ```
  - Execute the online query on the client machine, replace "host_ip" with the ip address of the server machine

   ```bash
   python3 tsm_eval_online.py --system monetdb --queries all --host "host_ip" --batch_size 10000 20000 200000 600000 1000000 1400000
   ```

   - Stop the system on the host machine
    ```bash
   sh stop.sh
   ```

    
- To produce the results of **QuestDB**
  -  Launch the system on the host machine 

   ```bash
   cd systems/questdb
   sh launch.sh
   ```
  - Execute the online query on the client machine, replace "host_ip" with the ip address of the server machine

   ```bash
   python3 tsm_eval_online.py --system questdb --queries all --host "host_ip" --batch_size 10000 20000 200000 
   ```

   - Stop the system on the host machine
    ```bash
   sh stop.sh
   ```   

- To produce the results of **TimescaleDB**
  -  Launch the system on the host machine 

   ```bash
   cd systems/timescaledb
   sh launch.sh
   ```
  - Execute the online query on the client machine, replace "host_ip" with the ip address of the server machine

   ```bash
   python3 tsm_eval_online.py --system timescaledb --queries all --host "host_ip" --batch_size 10000 20000 200000 600000 1000000 1400000
   ```

   - Stop the system on the host machine
    ```bash
   sh stop.sh
   ```   

<!---
**Notes**:

- The maximal batch_size depends on your architecture and the selected TSDB. **What does the reviewer need to do?**
- Druid supports ingestion and queries concurrently, while QuestDB does not support multithreading. **What does the reviewer need to do?**
- If you stop the program before its termination or shut down the system, the database might not be set into its initial state properly; you need to reload the dataset in the host machine: **What does the reviewer need to do?**

## Reproducing results for D-MULTI 

Run the following commands to produce the results for the larger dataset D-MULTI.

- Download and decompress Dataset 2 (takes ~90minutes)

```bash
cd ../datasets
sh build.sh d2
```

- Load Dataset 2 into the systems that can support it (takes ~ 36hours)

```bash
sh load_all.sh d2
```

- To reproduce the data bulk loading results in Table 3 for D-MULTI, run the following command:

```bash
sh repro_loading.sh
```

- To reproduce the offline workloads D-MULTI Q1-Q5 results (Figure 6), run the following command:

```bash
python3 tsm_eval.py --systems all --queries all --datasets d2
```


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
-->




