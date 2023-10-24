# TS-LSH: LSH-based Generation Technique for Long Time Series




## Install requirements

```bash
cd generation/
sh install.sh
```

You can generate new time series either using our pre-trained model or by retraining the model from scratch.  


## Option 1: Execution using pre-trained model      

```bash
python run_pretrained.py
```
The generated plots and data are stored in the `generation/results` folder.

## Option 2: Execution by training the model

  
### Data partitioning

- Partition your input data located in `data/` into segments of the same length

```bash
python ts_seg.py
```

### Model training

1. Train a GAN model on the original segments and write the generated segments into `results/` (takes ~10 days) 

```bash
cd gan/
python DCGAN.py
python encoder_dc.py
```

2. Generate new segments using the trained ones from Step 1
```bash
python test_dc.py
```

### Data generation

- Apply LSH to generate long time series 

```bash
python gen_ts.py
```
## Generation Examples:

![image](https://github.com/eXascaleInfolab/TSM-Bench/assets/15266242/13d8c2f9-fdbf-495f-aaf9-7f5ec0999470)



