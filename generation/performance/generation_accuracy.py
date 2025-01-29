#!/usr/bin/env python
# coding: utf-8

import json
import multiprocessing
import hashing.lsh_main as lsh
import time
from pathlib import Path
import pandas as pd
import random
import numpy as np
# import matplotlib.pyplot as plt
from tqdm import tqdm
import graph.random_walk_ori as random_walk
import lshashpy3 as lshash

# Load Data
data = pd.read_csv('data.csv')
data = data['data'].tolist()
data = data[:30000]

# Add noise
noise = np.random.normal(0, 0.015, len(data))
generated = list(data + noise)

# # Plot original and generated data
# plt.plot(data)
# plt.show()
# plt.plot(generated)
# plt.show()

# Create segments
window = 3072
segments = [generated[i:i + window] for i in range(0, len(generated) - window, int(0.1 * window))]

df_segments = pd.DataFrame(segments)
df_segments = df_segments.T

# # Plot segments
# df_segments.iloc[:, :50].plot(subplots=True, layout=(10, 6), figsize=(10, 10), legend=True, color='b')
# plt.show()

# Initialize LSH
lsh = lshash.LSHash(8, len(segments[0]), num_hashtables=8)

for i in segments:
    lsh.index(i)

# Query Data
to_query = [data[i:i + window] for i in range(0, len(data) - window, window)]
results = [lsh.query(to_query[i])[0][0][0] for i in range(len(to_query))]

# Process Results
res_lsh = []
for l in results:
    res_lsh += l

# # Plot LSH results
# plt.plot(res_lsh)
# plt.show()

# Distance function
def distance(a, b):
    return np.sqrt(np.sum((a - b)**2))

# Probability matrix function
def distopro(a):
    a = len(a)
    if a == 3:
        return np.array([0.2, 0.3, 0.5])
    elif a == 4:
        return np.array([0.1, 0.2, 0.3, 0.4])
    else:
        return np.array([0.04, 0.12, 0.2, 0.28, 0.36])

# Transform function
def transform(data, window_size, k):
    numOfSeq = data.shape[0]
    distance_matrix = np.ones([numOfSeq, numOfSeq], dtype=float)
    
    for i in range(numOfSeq):
        for j in range(numOfSeq):
            distance_matrix[i][j] = distance(data[i, data.shape[1] - window_size:], data[j, 0:window_size])
    
    relation_matrix = np.ones([numOfSeq, k], dtype=int)
    subdistance_matrix = np.ones([numOfSeq, k], dtype=float)
    probability_matrix = np.ones([numOfSeq, k], dtype=float)
    
    for i in range(numOfSeq):
        relation_matrix[i] = distance_matrix[i].argsort()[::-1][data.shape[0] - k:]
    
    for i in range(numOfSeq):
        for j in range(k):
            subdistance_matrix[i][j] = distance_matrix[i][relation_matrix[i][j]]
    
    for i in range(numOfSeq):
        probability_matrix[i] = distopro(subdistance_matrix[i])
    
    return distance_matrix, subdistance_matrix, relation_matrix, probability_matrix

# Random walk function
def next_step(relation_array, probability_array):
    value = random.random()
    threshold = [0]
    sum_value = 0
    
    for i in range(len(probability_array)):
        sum_value += probability_array[i]
        threshold.append(sum_value)
    
    for i in range(len(threshold) - 1):
        if threshold[i] < value <= threshold[i + 1]:
            return relation_array[i]

def random_walk(relation_matrix, probability_matrix, length):
    seq = [0]
    temp_id = 0
    
    for i in range(length - 1):
        temp_id = next_step(relation_matrix[temp_id], probability_matrix[temp_id])
        seq.append(temp_id)
    
    return np.array(seq)

# Execute Graph-Based Walk
seq = [0]
a, b, c, d = transform(np.array(segments), 100, 5)
path = random_walk(c, d, int(len(data) / window))
print(path)
# Process Graph-Based Walk Results
res_graph = []
for i in range(len(path)):
    #print(seq[i])
    res_graph += segments[path[i]]

# # Plot Graph-Based Walk Results
# plt.plot(segments[0])
# plt.show()

# Metrics Computation
import numpy as np
from scipy.stats import pearsonr
from sklearn.metrics import normalized_mutual_info_score, mean_squared_error

a = data[:len(res_graph)]
b = res_lsh
c = res_graph

# Compute Pearson Correlation
corr_ab, _ = pearsonr(a, b)
corr_ac, _ = pearsonr(a, c)

# Compute Normalized Mutual Information (NMI)
nmi_ab = normalized_mutual_info_score(a, b)
nmi_ac = normalized_mutual_info_score(a, c)

# Compute Root Mean Squared Error (RMSE)
rmse_ab = np.sqrt(mean_squared_error(a, b))
rmse_ac = np.sqrt(mean_squared_error(a, c))

# Save results to a text file
results = f"""
Correlation LSH: {corr_ab}
Correlation Graph: {corr_ac}

Normalized Mutual Information LSH: {nmi_ab}
Normalized Mutual Information Graph: {nmi_ac}

Root Mean Squared Error LSH: {rmse_ab}
Root Mean Squared Error Graph: {rmse_ac}
"""

with open("../../results/generation/experiment3_accuracy.csv", "w") as file:
    file.write(results)

print("Results saved.")

