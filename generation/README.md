# TS-LSH: LSH-based Generation Technique for Long Time Series




## Install requirements

```bash
cd generation/
sh install.sh
```

You can generate new time series using our pre-trained model or by retraining the model from scratch.  The latter takes a considerable amount of time.


## Option 1: Execution using pre-trained model      

```bash
python run_pretrained.py
```
The generated plots and data are stored in the `generation/results` folder.

## Option 2: Execution by training the model

  
### 1. Data Partitioning

- Partition your input data located in `data/` into segments of the same length

```bash
python ts_seg.py
```

### 2. Model Training

- Train a GAN model on the original segments and add the generated segments into `results/` (takes ~ 2 days) 

```bash
cd gan/
python DCGAN.py
python encoder_dc.py
```
- Generate new segments using the trained ones 
```bash
python test_dc.py
```

### 3. Data Generation

- Apply LSH to generate long time series 

```bash
cd ..
python gen_ts.py
```
## Generation Examples:

![image](https://github.com/eXascaleInfolab/TSM-Bench/assets/15266242/13d8c2f9-fdbf-495f-aaf9-7f5ec0999470)



