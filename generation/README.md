# TS-LSH: A LSH-based Generation Technique for Time Series

___
## Prerequisites

- Ubuntu 20.04 or higher
- Clone this repository

Build all databases using the installation script located in the root folder

```bash
sh install.sh
```
___
## Execution

### Training before Generation

The user has real-world data and wants to generate realistic synthetic time series. 

1. **[If no GAN model was trained yet]** The method takes in the real data segments under `data/` folder and trains a GAN model to learn its underlying characteristics (~ 3 days) 

```bash
python3 DCGAN.py
python3 encoder_dc.py
```

2. The method uses the trained GAN model under `generation/` folder to generate realistic synthetic segments into the same folder (~ 40 minutes)

```bash
python3 test_dc.py
```

3. The method uses the GAN synthetic under `generation/` folder  segments to generate long time series (~ 9 minutes)

```bash
python3 main.py
```

___
## Sample generation plots:

![plot_lsh_graph](https://github.com/eXascaleInfolab/TSM-Bench/assets/15266242/af057b32-37bc-4348-8699-730d7abd3ea7)

