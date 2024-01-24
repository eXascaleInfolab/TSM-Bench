from datetime import datetime

import pandas
import os
import numpy as np
import sys

sys.path.append(os.getcwd())
from utils.system_modules import system_module_map
from utils.query_template_loader import load_query_templates
import argparse
from numpy import random

"""


example usage:
From the root folder:
python3 misc/compression_from_dataset.py --d output.csv
"""


## Config
dataset_folder = "datasets"

repeats_percentages = [10, 30,70, 90]
scarsity_percentages = [10, 30, 60 , 80]
mean_deltas  = [1 , 3 ,  5  , 10]
outliers_n = [10, 30, 60, 80]

parser = argparse.ArgumentParser(description='Script for running any eval')
parser.add_argument('--dataset', "-d", nargs="?",
                    type=str, required=True)
args = parser.parse_args()

dataset_folder = "datasets"
dataset = args.dataset

if dataset.endswith(".csv"):
    dataset = dataset[:-4]

print("loading dataset", dataset)

df = pandas.read_csv(f"{dataset_folder}/{dataset}.csv")

# format time column (the fist one to 2019-03-01T00:00:30)
df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: datetime.strptime(x.replace(".000000000", "").strip().replace(" ", "T"), "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S"))
print(df.head())

random.seed(42)


def generate_repeats(ts, repeats_percentage):
    repeats_percentage = max(0, min(100, repeats_percentage))
    for i in range(len(ts)):
        if i == 0:
            continue
        if random.randint(0, 99) < repeats_percentage:
            ts[i] = ts[i - 1]
    return ts


def generate_outliers(ts, outliers_percentage):
    outliers_percentage = max(0, min(100, outliers_percentage))
    for i in range(len(ts)):
        if random.randint(0, 99) < outliers_percentage:
            ts[i] = ts[i] + np.random.normal(10, 5)
    return ts


def generate_scarsity(ts, scarsity_percentage):
    scarsity_percentage = max(0, min(100, scarsity_percentage))
    for i in range(len(ts)):
        if random.randint(0, 99) < scarsity_percentage:
            ts[i] = None
    return ts


def generate_delta(ts, mean_delta):
    lags = np.diff(ts)
    current_mean_delta = np.mean(np.abs(lags))
    new_lags = mean_delta / current_mean_delta * lags

    for i, _ in enumerate(ts):
        if i == 0:
            continue
        ts[i] = ts[i - 1] + new_lags[i - 1]
    # print("new delta mean", np.mean(np.abs(np.diff(ts))))
    return ts


station_ids = sorted(list(set(df.iloc[:, 1].values)))

import matplotlib.pyplot as plt
plot_folder = "results/compression_plots"
os.makedirs(plot_folder, exist_ok=True)


for repeats_percentage in repeats_percentages:
    new_df = df.copy()
    for i in range(2, 100 + 2):
        for station_id in station_ids:
            station_indices = np.arange(df.shape[0])[new_df.iloc[:, 1] == station_id]
            ts = new_df.iloc[station_indices, i].values
            new_df.iloc[station_indices, i] = generate_repeats(ts, repeats_percentage).round(decimals=6)

    new_df.to_csv(f"{dataset_folder}/repeats_{repeats_percentage}.csv", index=False, header=True)
    new_df.iloc[station_indices[:2000], i].plot(title=f"repeats_{repeats_percentage}")
    plt.savefig(f"{plot_folder}/repeats_{repeats_percentage}.png")
    plt.clf()


for mean_delta in mean_deltas:
    new_df = df.copy()
    for i in range(2, 100 + 2):
        for station_id in station_ids:
            station_indices = np.arange(df.shape[0])[new_df.iloc[:, 1] == station_id]
            ts = new_df.iloc[station_indices, i].values
            new_df.iloc[station_indices, i] = generate_delta(ts, mean_delta).round(decimals=6)

    new_df.to_csv(f"{dataset_folder}/delta_{mean_delta}.csv", index=False, header=True)
    new_df.iloc[station_indices[:2000], i].plot(title=f"delta_{mean_delta}")
    plt.savefig(f"{plot_folder}/delta_{mean_delta}.png")
    plt.clf()


for scarsity_percentage in scarsity_percentages:
    new_df = df.copy()
    for i in range(2, 100 + 2):
        for station_id in station_ids:
            station_indices = np.arange(df.shape[0])[new_df.iloc[:, 1] == station_id]
            ts = new_df.iloc[station_indices, i].values
            new_df.iloc[station_indices, i] = generate_scarsity(ts, scarsity_percentage).round(decimals=6)

    new_df.to_csv(f"{dataset_folder}/scarsity_{scarsity_percentage}.csv", index=False, header=True)
    new_df.iloc[station_indices[:2000], i].plot(title=f"scarsity_{scarsity_percentage}")
    plt.savefig(f"{plot_folder}/scarsity_{scarsity_percentage}.png")
    plt.clf()
