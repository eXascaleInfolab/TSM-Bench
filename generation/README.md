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
python3 run_pretrained.py
```

## Execution with model training

### Model Training

- **Step 1: ** Train a GAN model on data segments located in `data/` and write the resulting segments into `generation/` (takes ~3 days) 

```bash
python3 DCGAN.py
python3 encoder_dc.py
```

- **Step 2: ** Generate new segments using the trained ones from Step 1 (takes ~46 seconds)

```bash
python3 test_dc.py
```
### Time Series Generation

- **Step 3: ** Apply LSH to generate long time series (takes ~20 seconds)

```bash
python3 gen_ts.py
```




___
## Sample generation plots:

![image](https://github.com/eXascaleInfolab/TSM-Bench/assets/15266242/13d8c2f9-fdbf-495f-aaf9-7f5ec0999470)

