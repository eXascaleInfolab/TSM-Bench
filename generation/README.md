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
## Execution

1. The method takes in synthetic segments and generates seed sequences (~ 3 days)

```bash
python3 DCGAN.py
python3 encoder_dc.py
python3 test_dc.py
```

2. The method uses the synthetic segments to generate long time series (~ 9 minutes)

```bash
python3 main.py
```

___
## Sample generation plots:

![plot_lsh_graph](https://github.com/eXascaleInfolab/TSM-Bench/assets/15266242/af057b32-37bc-4348-8699-730d7abd3ea7)

