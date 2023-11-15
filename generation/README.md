# TS-LSH: LSH-based Generation Technique for Long Time Series

TS-LSH is a scalable data generator that closely emulates the properties of real-world time series. One of the benefits of this tool is to facilitate data sharing for benchmarking tasks, particularly when datasets are non-public due to privacy issues.  Our method relies on Generative Adversarial Network (GAN) to create large volumes of time series data. 
You can generate new time series using our pre-trained model (Option 1) or by retraining the model from scratch (Option 2). 
The generated plots and data will be saved in the `generation/results` folder.

## Generation Examples

![image](https://github.com/eXascaleInfolab/TSM-Bench/assets/15266242/13d8c2f9-fdbf-495f-aaf9-7f5ec0999470)



## Setup
- Install the necessary dependencies using the following script:

```bash
cd generation/
sh install.sh
```


## Arguments:

- You can customize the time series generation using the following parameters:

   - `--len_ts` (optional, integer): The length of time series; default: 10K datapoints.
   - `--nb_ts` (optional, integer): The number of time series; default: 3 time series.
   - `--seed` (optional, string): A link to the original file; default: _bafu_.

## TS-LSH Usage

### Option 1: Generation using pre-trained model      


```bash
   python run_pretrained.py
```
- Example: Generate 10 time series with 100K datapoints each: 

```bash
   python run_pretrained.py --len_ts 100000 --nb_ts 10 --seed conductivity
```


### Option 2: Generation using a custom dataset

 
#### 1. Create dataset folder 

- Create a new folder under `data/` under the name of your dataset and place your dataset file inside it such as: `data/{your_dataset_name}/original.txt`.

#### 2. Model Training

- Train a GAN model on the original segments and add the generated segments into `results/` (takes ~ 2 days) 

```bash
cd gan/
python DCGAN.py --seed {your_dataset_name}
python encoder_dc.py --seed {your_dataset_name}
```
- Generate new segments using the trained ones 
```bash
python test_dc.py --seed {your_dataset_name}
```

#### 3. Data Generation

```bash
cd ..
python gen_ts.py  --seed {your_dataset_name}
```
- Example: Generate 10 time series with with 100K datapoints each:

```bash
python gen_ts.py --len_ts 100000 --nb_ts 10 --seed {your_dataset_name}
```
  
<!--
Apply LSH to generate long time series using ```gen_ts.py```. To use this script, the following arguments and examples are provided:

- `--len_ts` (optional, integer): The length of ts.
- `--nb_ts` (optional, integer): The number of ts.
- `--fori` (optional, string): A link to the original file.
- `--fsynth` (optional, string): A link to the synthetic segments.
- `--output_to` (optional, string): A link to the exported generated file.

1. Running the script with default values:

   ```bash
   python gen_ts.py
    ```
1. Generate 10 time series with 100K datapoints each:

```bash
   python gen_ts.py --len_ts 100000 --nb_ts 10
```
The generated plots and data are stored in the `generation/results` folder.
-->





