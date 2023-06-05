# User Defined Functions (UDFs)

We have also implemented additional time series tasks using **User Defined Functions (UDFs)**. Those queries involve a mix of matrix operations and iterative procedures, which are very hard to implement in the native language. We consider the following tasks: data normalization, matrix decomposition, anomaly detection, anomaly repair, clustering, and classification. Furthermore, we have implemented various missing values imputation techniques from a recent benchmark.
___

## Running evals

| Database | Algorithm | Datasets |
| ------ | ------ | ------ |
| extremedb | cd| d1 |
| monetdb | dist | d2 |
| timescaledb | dstree |  |
|  | hotsax |  |
|  | kmeans | |
|  | knn | |
|  | knn-operators | |
|  | records-select-long | |
| | recovdb | |
| | sax-representation | |
| | screen | |
| | simple-queries | |
| | sum-long | |
| | z-normalization | |
| | z-normalization-operators | |

___
## Examples of Running evaluations

Make sure first that the evaluated system-s is/are running before launching the UDF performanec evaluation

Insert time and throughput is taken for each run. It is a double check that the data has been inserted

##### Runtime of Similarity Search [DS-Tree]


```bash
python3 run_eval.py --dataset d1 --algorithm dist --database timescaledb
```

##### Runtime of SAX representation [Mapping]

```bash
python3 run_eval.py --dataset d1 --algorithm sax-representation --database timescaledb
```



##### Runtime of Centroid Decomposition [Decomposition]

```bash
python3 run_eval.py --dataset d1 --algorithm cd --database timescaledb
```



##### Runtime of recovery of missing values [RecovDB]

```bash
python3 run_eval.py --dataset d1 --algorithm recovdb --database timescaledb
```

##### Runtime of K-Means [Clustering]

```bash
python3 run_eval.py --dataset d1 --algorithm kmeans --database timescaledb
```


##### Runtime  of KNN [Classification]

```bash
python3 run_eval.py --dataset d1 --algorithm knn --database timescaledb
```


##### Runtime  of Hot-Sax [Anomaly Detection]

```bash
python3 run_eval.py --dataset d1 --algorithm hotsax --database timescaledb
```

___
## Running eval

Each of the databases has a dedicated directory in Databases. In them, there is a dedicated directory for each experiment. In order to run an experiment, go to the directory of the experiment and use the Python3 script there. For example,

```bash
$ cd systems/{system}/
$ python3 generate_udf.py
```

Note that the scripts can be configured to run on different datasets and different dimensions. For example,
```bash
$ cd systems/{systems}/
$ python3 generate_udf.py --file <path_to_file> 
```
