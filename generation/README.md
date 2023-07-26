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
## Step 1: Generating synthetic segments using GAN

### Introduction

The objective of this step is to generate seed fragments (sequences) from real-time sequence data, which is constrained by size.

In the following, we use DCGAN used by TS-Benchmark, but any GAN variant could be used. 

### Start

Access the GAN folder ``cd gan/``:

1. Train DCGAN model ``python3 DCGAN.py``

2. Train the encoder model ``python3 encoder_dc.py``

3. Execute benchmark  ``python3 test_dc.py``

The GAN training time varied depending on the number of iterations, the number of segments, and the size of segments.

In the end of the training process, GAN would generate generated segments to a file ``synthetic_segments.txt``.

___
## Step 2: Generating long time series

### Running TS-LSH

This step constructs locality-sensitive hashing (LSH) tables and indexes the GAN-generated segments. It then uses the original data to query the hashing tables to obtain similar synthetic time series segments. Finally, it appends the results to the long generated time series. 

The following scripts would execute all previous steps in addition to the state-of-the-art method Graph-GAN:

<pre><code>
python3 main.py
</code></pre>

___
## Sample generation plots:

![image](https://github.com/eXascaleInfolab/TSM-Bench/assets/15266242/4a590799-222b-4c52-ac21-3550bfe71f24)
