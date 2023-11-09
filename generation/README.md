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

Apply LSH to generate long time series using ```gen_ts.py```. To use this scipt, the following arguments and examples are provided:

- `--len_ts` (optional, integer): The length of ts.
- `--nb_ts` (optional, integer): The number of ts.
- `--fori` (optional, string): A link to the original file.
- `--fsynth` (optional, string): A link to the synthetic segments.
- `--output_to` (optional, string): A link to the exported generated file.

1. Running the script with default values:

   ```bash
   python gen_ts.py
    ```
1. Generate 10 time series with a million datapoints each:: 

   ```bash
   python gen_ts.py --len_ts 100000 --nb_ts 10
    ```


## Generation Examples:

![image](https://github.com/eXascaleInfolab/TSM-Bench/assets/15266242/13d8c2f9-fdbf-495f-aaf9-7f5ec0999470)



