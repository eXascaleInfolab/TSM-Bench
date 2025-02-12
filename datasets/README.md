# Datasets

## Description
We use as seed a real-world dataset of water temperature and level time series recorded using multiple hydrometric sensors. Temperature series contain duplicates and similar consecutive values while level series are erratic and contain abrupt changes. We augment the seed dataset by scaling i) the number of time series—we increase the number of stations and/or sensors—and ii) the length of time series—we increase their duration.

We use our LSH-GAN data generator to augment the size of the seed dataset into two larger datasets. The dimensions of the two datasets used in the benchmark are the following:

| dataset | # of TS | # of Stations | # of Sensors per station | Length of TS | 
| ------ | ------ | ------ | ------ | ------ |
| d1 | 1K | 10 | 100 | 5.18M |
| d2 | 200K | 2000 | 100 | 17.2B


## Datasets Building 

Due to size limitations, we upload only d1 in a compressed format. To download the two datasets as a csv format, run the following building script:

- Build Dataset 1 (takes ~ 10 mins)

```bash
sh build.sh d1

```

- Build Dataset 2 (takes a considerable time)

```bash
sh build.sh d2

```

## Source

The seed dataset was kindly provided by the [Federal Office for the Environment in Switzerland (FOEN)](https://www.bafu.admin.ch/bafu/en/home/topics/water.html).




 

<!---
  

___
## Building the datasets 

The two datasets are uploaded as ... and are located under ... 


- To download the datasets, run the following install script:

```bash
$ sh build_{dataset}.sh
```
- Note: You need to replace ```{dataset}``` with one of the datasets from the table above.


-->
