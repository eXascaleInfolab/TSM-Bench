# TS-LSH : A LSH-based Generation Technique for Time Series

___
## Prerequisites

- Ubuntu 20.04 or higher
- Clone this repository

Build all databases using the installation script located in the root folder

```bash
sh install.sh
```
___
## Sample Data

A csv formatted time series data as following can be used: 

<pre><code>
time,series1,series2 ... 
1,11.1,21.1 .. 
2,12.2,22.2 .. 
3,13.0,23.1 .. 
     .
     .
     .
</code></pre>

The file path should be put in the parameters files: *parameters.json*. 


___
## Step 1: Generating synthetic segments

### Introduction

The objective of this step is to generate seed fragments (sequences) from real-time sequence data, which is often constrained by data size limitations.

### Start

Access the gan/ folder: ``cd gan/``:

1. first train DCGAN model ``python3 DCGAN.py``

2. then train the encoder model ``python3 encoder_dc.py``

3. execute benchmark  ``python3 test_dc.py``


___
## Step 2: Generating long time series

### Running TS-LSH

This step constructs locality-sensitive hashing (LSH) tables and indexes the GAN-generated segments. It then uses the original data to query the hashing tables to obtain similar synthetic time series segments. Finally, it appends the o 

<pre><code>
python3 main.py
</code></pre>

to run the TS-LSH pipeline, this will decompose the time series data using the STL-Robust decomposition,
train a model for each component, generate new time series data then reconstruct the time series data. 

