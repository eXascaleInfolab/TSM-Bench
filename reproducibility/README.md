 # Reproducibility for TSM-Bench
 
**Paper**: Abdelouahab Khelifati, Mourad Khayati, Anton Dignös, Djellel Difallah, and Philippe Cudré-Mauroux: [TSM-Bench: Benchmarking Time Series Database Systems for Monitoring Applications](https://www.vldb.org/pvldb/vol16/p3363-khelifati.pdf). PVLDB 2023.
- **Systems**: The benchmark evaluates all the systems mentioned in the paper: TSM-Bench, [ClickHouse](https://clickhouse.com/), [Druid](https://druid.apache.org/), [eXtremeDB](https://www.mcobject.com/)*, [InfluxDB](https://docs.influxdata.com/influxdb/v1.7/), [MonetDB](https://www.monetdb.org/easy-setup/), [QuestDB](https://questdb.io/), [TimescaleDB](https://www.timescale.com/).
- **Datasets**: The benchmark evaluates the two datasets for the evaluation: *D-LONG [d1] and D-MULTI [d2]*. The evaluated datasets can be found [here](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/datasets).
- **Workloads**: This code evaluates the workloads performed in the paper including: Data Bulk Loading, Offline Queries, Online Queries, Generation Performance and Feature Evaluation.
- <sup>*</sup>**Note**: Due to license restrictions, we can only share the evaluation version of extremeDB. The results between the benchmarked and the public version might diverge. 

[**Prerequisites**](#prerequisites) | [**Installation**](#systems-setup) | [**Datasets Loading**](#datasets-loading) | [**Experiments**](#experiments) | [**Benchmark Extension**](#benchmark-extension) | [**Technical Report**](#technical-report) | [**Data Generation**](#time-series-generation)


- Ubuntu 22 (including Ubuntu derivatives, e.g., Xubuntu); 128 GB RAM
- Clone this repository (this can take a couple of minutes as it uploads one of the datasets)
- Mono: Install mono from https://www.mono-project.com/download/stable/ (takes a few minutes).

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


- Download and decompress Dataset 1 (takes ~ 3mins)

```bash
cd ../datasets
sh build.sh d1
```

- Load Dataset 1 into all the systems (takes ~ 2hours)

```bash
sh load_all.sh d1
```


## Data Bulk Loading & Compression (Table 3 in paper):

- To reproduce the data bulk loading results in Table 3, run the following command:

```bash
sh repro_table3.sh
```
    
## Offline Workloads D-LONG Q1-Q7 (Figures 3, 4, and 5):

To reproduce the offline workloads D-LONG Q1-Q7 results, execute the following command (takes ~ 3hours):

```bash
python3 tsm_eval.py --systems all --queries all --datasets d1 
```


## Online Workloads D-LONG Q1-Q5 (Figure 8):

To reproduce the online workloads Q1-Q5 results, use the following command:

[command]



## Data Generation Performance (Figure 9):

To reproduce the data generation performance results, execute the following command:

[command]


## Compression Performance (Figure 10):

To reproduce the compression performance results, run the following command:

[command]


## Reproducing results for D-MULTI (Longer Runtime)

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
sh repro_table3.sh
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



