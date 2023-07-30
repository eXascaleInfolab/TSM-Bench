# User Defined Functions (UDFs)

We have also implemented additional time series tasks using **User Defined Functions (UDFs)**. The implemented queries involve a mix of matrix operations and iterative procedures, which are very hard to implement in the native language. We consider the following tasks: Similarity Search [DS-Tree], Time Series Representation [SAX], Matrix Decomposition [Centroid Decomposition], Recovery of Missing Values [RecovDB], Clustering [K-Means], Classification [KNN], Anomaly Detection [Hot-Sax].
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

- Make sure first that the evaluated system is running before launching the UDF performance evaluation

- Insertion time and throughput are computed for each run. It is a double check that the data has been inserted

### Similarity Search [DS-Tree]


```bash
python3 run_eval.py --dataset d1 --algorithm dist --database timescaledb
```

### Time Series Representation [SAX]

```bash
python3 run_eval.py --dataset d1 --algorithm sax-representation --database timescaledb
```



### Matrix Decomposition [Centroid Decomposition]

```bash
python3 run_eval.py --dataset d1 --algorithm cd --database timescaledb
```



### Recovery of Missing Values [RecovDB]

```bash
python3 run_eval.py --dataset d1 --algorithm recovdb --database timescaledb
```

### Clustering [K-Means]

```bash
python3 run_eval.py --dataset d1 --algorithm kmeans --database timescaledb
```


### Classification [KNN]

```bash
python3 run_eval.py --dataset d1 --algorithm knn --database timescaledb
```


### Anomaly Detection [Hot-Sax]

```bash
python3 run_eval.py --dataset d1 --algorithm hotsax --database timescaledb
```

___
## Running eval

In order to run an experiment:

```bash
$ python3 generate_udf.py
```

The scripts can be configured to run on different datasets and different dimensions. For example,
```bash
$ cd systems/{systems}/
$ python3 generate_udf.py --file <path_to_file> 
```
