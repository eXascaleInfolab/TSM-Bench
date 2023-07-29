# TS-LSH: LSH-based Generation Technique for Long Time Series

<!---

___
## Prerequisites

- Ubuntu 20.04 or higher
- Clone this repository

Build all databases using the installation script located in the root folder

```bash
sh install.sh
```
___

-->

## Execution with a pre-trained model 


```bash
python3 gen_ts.py
```

## Execution with model training

### Model Training

- Train a GAN model on data segments located in `data/` and write the resulting segments into `generation/` (takes ~3 days) 

```bash
python3 DCGAN.py
python3 encoder_dc.py
```

- Generate new segments using the trained ones from Step 1 (takes ~40 minutes)

```bash
python3 test_dc.py
```
### Time Series Generation

- Apply LSH to generate long time series (takes ~9 minutes)

```bash
python3 gen_ts.py
```




___
## Sample generation plots:

![plot_lsh_graph](https://github.com/eXascaleInfolab/TSM-Bench/assets/15266242/af057b32-37bc-4348-8699-730d7abd3ea7)

