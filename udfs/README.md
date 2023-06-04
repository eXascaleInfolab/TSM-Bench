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
## Examples of Running evals based on figures in the work

Make sure first that the evaluated system-s is/are running before launching the UDF performanec evaluation

Insert time and throughput is taken for each run. It is a double check that the data has been inserted

##### Similarity Search.


```bash
python3 run_eval.py --dataset d1 --lines 1000000 --columns 46 --algorithm dist --database timescaledb
python3 run_eval.py --dataset d1 --lines 1000000 --columns 46 --algorithm dist --database monetdb
python3 run_eval.py --dataset d1 --lines 1000000 --columns 46 --algorithm dist --database extremedb
```

##### Runtime of SAX representation.

d1

```bash
python3 run_eval.py --dataset d1 --lines 750000 --columns 46 --algorithm sax-representation --database timescaledb
python3 run_eval.py --dataset d1 --lines 750000 --columns 46 --algorithm sax-representation --database monetdb
python3 run_eval.py --dataset d1 --lines 750000 --columns 46 --algorithm sax-representation --database extremedb
```



##### Runtime of Centroid Decomposition.

d1

```bash
python3 run_eval.py --dataset d1 --lines 100000 --columns 46 --algorithm cd --database timescaledb
python3 run_eval.py --dataset d1 --lines 100000 --columns 46 --algorithm cd --database monetdb
python3 run_eval.py --dataset d1 --lines 100000 --columns 46 --algorithm cd --database extremedb
```



##### FIGURE 4.11 Runtime of recovery of missing values (QB4).

d1

```bash
python3 run_eval.py --dataset d1 --lines 100000 --columns 46 --algorithm recovdb --database timescaledb
python3 run_eval.py --dataset d1 --lines 100000 --columns 46 --algorithm recovdb --database monetdb
python3 run_eval.py --dataset d1 --lines 100000 --columns 46 --algorithm recovdb --database extremedb


##### Runtime of data repair algorithm – K-Means.

d1

```bash
python3 run_eval.py --dataset d1 --lines 1000000 --columns 46 --algorithm kmeans --database timescaledb
python3 run_eval.py --dataset d1 --lines 1000000 --columns 46 --algorithm kmeans --database monetdb
python3 run_eval.py --dataset d1 --lines 1000000 --columns 46 --algorithm kmeans --database extremedb
```


##### Runtime  of KNN

d1

```bash
python3 run_eval.py --dataset d1 --lines 5000 --columns 46 --algorithm knn --database timescaledb
python3 run_eval.py --dataset d1 --lines 5000 --columns 46 --algorithm knn --database monetdb
python3 run_eval.py --dataset d1 --lines 5000 --columns 46 --algorithm knn --database extremedb
```


##### Runtime of KNN using database operators

```bash
python3 run_eval.py --dataset d1 --lines 10000 --columns 46 --algorithm knn-operators --database timescaledb
python3 run_eval.py --dataset d1 --lines 10000 --columns 46 --algorithm knn-operators --database monetdb
python3 run_eval.py --dataset d1 --lines 10000 --columns 46 --algorithm knn-operators --database extremedb
```

##### Runtime of Anomalies detection 

d1

```bash
python3 run_eval.py --dataset d1 --lines 2000 --columns 46 --algorithm hotsax --database timescaledb
python3 run_eval.py --dataset d1 --lines 2000 --columns 46 --algorithm hotsax --database monetdb
python3 run_eval.py --dataset d1 --lines 2000 --columns 46 --algorithm hotsax --database extremedb
```

##### Runtime of Similiarity search 

```bash
python3 run_eval.py --dataset d2 --lines 2205 --columns 5000 --algorithm hotsax --database timescaledb
python3 run_eval.py --dataset d2 --lines 2205 --columns 5000 --algorithm hotsax --database monetdb
python3 run_eval.py --dataset d2 --lines 2205 --columns 5000 --algorithm hotsax --database extremedb
```

___
## Running eval

Each of the databases has a dedicated directory in Databases. In them, there is a dedicated directory for each experiment. In order to run an experiment, go to the directory of the experiment and use the Python3 script there. For example,

```bash
$ cd systems/{systems}/
$ python3 generate_udf.py
```

Note that the scripts can be configured to run on different datasets and different dimensions. For example,
```bash
$ cd systems/{systems}/
$ python3 generate_udf.py --file <path_to_file> --lines 1000 --columns 50
```
