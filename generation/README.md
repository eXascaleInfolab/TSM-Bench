# TS-LSH: LSH-based Generation Technique for Long Time Series


### Install Requirements

```bash
cd generation
install.sh
```

### Execution using a Pre-trained Model 

```bash
python3 run_pretrained.py
```
The generated plots and data are stored in the `generation/results` folder.

### Execution using Model Training

  
#### Step 1: Data Partionning

- Partition your input data located in `data/` into segments of the same length

```bash
python3 ts_seg.py
```

#### Step 2: Model Training

1. Train a GAN model on the original segments and write the generated segments into `generation/` (takes ~3 days) 

```bash
python3 DCGAN.py
python3 encoder_dc.py
```

2. Generate new segments using the trained ones from Step 1 (takes ~46 seconds)

```bash
python3 test_dc.py
```
#### Step 3: Data Generation

- Apply LSH to generate long time series (takes ~20 seconds)

```bash
python3 gen_ts.py
```
### Sample Generation Plots:

![image](https://github.com/eXascaleInfolab/TSM-Bench/assets/15266242/13d8c2f9-fdbf-495f-aaf9-7f5ec0999470)

