# User Defined Functions (UDFs)

We have also implemented additional time series tasks using **User Defined Functions (UDFs)**. The implemented queries involve a mix of matrix operations and iterative procedures, which are very hard to implement in the native language. We consider the following tasks: Similarity Search, Time Series Representation, Matrix Decomposition, Recovery of Missing Values, Clustering, Classification, and Anomaly Detection.
___

### UDFs Execution 

- UDF executions for all systems can be executed as follows:

	```bash
	python3 run_eval.py [args]
	```

- **Mandatory Arguments**: [args] should be replaced with the name of the system, query, and dataset:  


| --system | --algorithm | --datasets |
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

- **Examples of running UDFs**:

Make sure first that the evaluated system is running before launching the UDF performance evaluation

1.  Similarity Search [DS-Tree]


```bash
python3 run_eval.py --dataset d1 --algorithm dist --database timescaledb
```

2. Time Series Representation [SAX]

```bash
python3 run_eval.py --dataset d1 --algorithm sax-representation --database timescaledb
```

3. Matrix Decomposition [Centroid Decomposition]

```bash
python3 run_eval.py --dataset d1 --algorithm cd --database timescaledb
```



4. Recovery of Missing Values [RecovDB]

```bash
python3 run_eval.py --dataset d1 --algorithm recovdb --database timescaledb
```

5. Clustering [K-Means]

```bash
python3 run_eval.py --dataset d1 --algorithm kmeans --database timescaledb
```


6. Classification [KNN]

```bash
python3 run_eval.py --dataset d1 --algorithm knn --database timescaledb
```


7. Anomaly Detection [Hot-Sax]

```bash
python3 run_eval.py --dataset d1 --algorithm hotsax --database timescaledb
```
