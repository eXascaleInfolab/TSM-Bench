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

Any csv formatted time series data as following can be used: 

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
## Part 1: Generating synthetic segments

### Introduction

The main function of this module is to simulate and generate credible time series data.
In order to simulate time series more effectively and generate time series more effectively, we propose a massive time series data generation framework, which has the following steps:
Creating seed fragments (sequences) based on real-time sequence data usually limits the data size.

- Use certain generative adversarial network (GAN) models to generate synthetic fragments from real seeds.
- Create a directed graph of synthesized fragments.
- On the directed graph of the synthesized segment. Use random walk algorithm to generate continuous time series

### Start

1. first train DCGAN model ``python DCGAN.py``

2. then train the encoder model ``python encoder_dc.py``

3. execute benchmark  ``python test_dc.py``


___
## Part 2: Generating long time series

### Running TS-LSH

<pre><code>
python main.py
</code></pre>
to run the TS-LSH pipeline, this will decompose the time series data using the STL-Robust decomposition,
train a model for each component, generate new time series data then reconstruct the time series data. 

