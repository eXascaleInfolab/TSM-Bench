# sigmod15-screen
Code release of ["SCREEN: Stream Data Cleaning under Speed Constraints." (SIGMOD 15)](https://dl.acm.org/citation.cfm?doid=2723372.2723730).
The description of code files are listed below:

- `Screen.java`: Algorithm 1 in the paper. Use SCREEN algorithm to repair time series with certain speed constraints.
- `TimePoint.java`: the class for TimePoint indicating a time point.
- `TimeSeries.java`: the class for TimeSeries indicating a time sereis.

Datasets
----------
The public datasets in the paper:

- [STOCK](http://finance.yahoo.com/q/hp?s=AIP.L+Historical+Prices) with synthetic errors.

The schema of the data file contains three columns, 

- timestamp: the timestamp of the data
- dirty: the observation
- truth: the truth

Attention

- The example dataset is `data/stock10k.data`, in case the link is out of date

Parameters
----------
The input and output of **Screen** algorithm is:

Method

```
Screen(dirtySeries, sMax, sMin, T)
mainScreen()
```

Input:

```
double sMax = 6           // maximum speed
double sMin = -6          // minimum speed
long T = 1                // window size
TimeSeries dirtySeries
```

Output

```
Timeseries resultSeries
```

Typos in the draft
----------
Sorry for the typos in the draft in Section 3.2.1, page 4.
Above formula (7), the equations of $|xi-xi'|$ should be modified as follows:

```
xi-xk'+smax(tk-ti)
xk'-xi-smin(tk-ti)
0
```

Citation
----------
If you use this code for your research, please consider citing:

```
@inproceedings{DBLP:conf/sigmod/SongZWY15,
  author    = {Shaoxu Song and
               Aoqian Zhang and
               Jianmin Wang and
               Philip S. Yu},
  title     = {{SCREEN:} Stream Data Cleaning under Speed Constraints},
  booktitle = {Proceedings of the 2015 {ACM} {SIGMOD} International Conference on
               Management of Data, Melbourne, Victoria, Australia, May 31 - June
               4, 2015},
  pages     = {827--841},
  year      = {2015}
}
```
