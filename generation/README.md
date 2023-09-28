# TS-LSH: LSH-based Generation Technique for Long Time Series


### Install requirements

```bash
cd generation
install.sh
```

### Execution using a pre-trained model 

```bash
python3 run_pretrained.py
```
The generated plots and data are stored in the `generation/results` folder.

### Execution by retraining the model

  
#### Step 1: Data partitioning

- Partition your input data located in `data/` into segments of the same length

```bash
python3 ts_seg.py
```

#### Step 2: Model training

1. Train a GAN model on the original segments and write the generated segments into `results/` (takes ~3 days) 

```bash
python3 DCGAN.py
python3 encoder_dc.py
```

2. Generate new segments using the trained ones from Step 1 (takes ~46 seconds)

```bash
python3 test_dc.py
```

#### Step 3: Data generation

- Apply LSH to generate long time series (takes ~20 seconds)

```bash
python3 gen_ts.py
```
### Sample Generation plots:

![image](https://github.com/eXascaleInfolab/TSM-Bench/assets/15266242/13d8c2f9-fdbf-495f-aaf9-7f5ec0999470)

