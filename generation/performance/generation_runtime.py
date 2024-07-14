#!/usr/bin/env python
# coding: utf-8

import json
import multiprocessing
import time
from pathlib import Path
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import graph.random_walk_ori as random_walk
import lshashpy3 as lshash
import math 
from scipy import stats
from scipy.signal import lfilter

def sigmoid(x):
    return 1 / (1 + math.exp(-x))


import os

# Create results/generation directory if it doesn't exist
output_dir = Path("../../results/generation")
output_dir.mkdir(parents=True, exist_ok=True)

def moving_avg(x, n):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[n:] - cumsum[:-n]) / float(n)

window = 3072
nTS = 3
percentage_reconst = 70

data = pd.read_csv('Electric.csv')
data = data['Electric'].tolist()
data = stats.zscore(np.array(data))
data = data.tolist()
len(data)

df_segments = pd.read_csv('fake0.csv', header=None)
df_segments = df_segments.T

n = 10
b = [1.0 / n] * n
a = 1

for col in tqdm(df_segments):
    yy = lfilter(b, a, df_segments[col].tolist())
    yy[:n] = yy[n:n+1]
    df_segments[col] = yy.tolist()

df_segments.iloc[:, :50].plot(subplots=True, layout=(10, 6), figsize=(10, 10), legend=True, color='b')
plt.show()

segments = [df_segments[col].tolist() for col in df_segments]
print(len(segments))

def LSH(ori, generated, window, nTS, n_top=30, hash_length=window//300, num_hashtables=8):
    lsh = lshash.LSHash(hash_length, window, num_hashtables=num_hashtables)
    for i in generated:
        lsh.index(i)
    to_query = [ori[i:i + window] for i in range(0, len(ori) - window, window)]
    lsh_res = []
    k = int(window * .03)
    for i in tqdm(range(nTS)):
        temp = to_query[0]
        for i in range(1, len(to_query)):
            candidates = lsh.query(to_query[i], distance_func="euclidean", num_results=n_top)
            s = list(to_query[i])
            temp_t = temp[-k:]
            s_h = s[:k]
            overlap = [(1 - sigmoid(i)) * temp_t[i + k//2] + sigmoid(i) * s_h[i + k//2] for i in range(-k//2, k//2)]
            temp[-k:] = overlap
            s[:k] = overlap[::-1]
            temp.extend(s)
        lsh_res.append(temp)
    return lsh_res

def LSH_update(ori, generated, window, nTS, n_top=30, hash_length=window//300, num_hashtables=8):
    lsh = lshash.LSHash(hash_length, window, num_hashtables=num_hashtables)
    for i in generated:
        lsh.index(i)
    to_query = [ori[i:i + window] for i in range(0, len(ori) - window, window)]
    lsh_res = []
    used = 0
    k = int(window * .03)
    lsh_output = {}
    start = time.time()
    for i in tqdm(range(nTS)):
        current = i
        temp = to_query[0]
        for i in range(1, len(to_query)):
            candidates = None
            while candidates is None:
                try:
                    candidates = lsh.query(to_query[i], distance_func="euclidean", num_results=n_top)
                except:
                    pass
            s = list(to_query[i])
            temp.extend(s)
            used += 1
        lsh_res.append(temp)
        if used > len(generated) * percentage_reconst // 100:
            used = 0
            lsh_output[current] = time.time() - start
            print(lsh_output)
            print('lsh reconstruction...')
            lsh = lshash.LSHash(hash_length, window, num_hashtables=num_hashtables)
            for i in generated:
                lsh.index(i)
    return lsh_res, lsh_output

def distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

def distopro(a):
    if len(a) == 3:
        return np.array([0.2, 0.3, 0.5])
    elif len(a) == 4:
        return np.array([0.1, 0.2, 0.3, 0.4])
    else:
        return np.array([0.04, 0.12, 0.2, 0.28, 0.36])

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

def Graph(ori, generated, window, nTS):
    a, b, c, d = transform(np.array(generated), 100, 5)
    graph_res = []
    for i in range(nTS):
        path = random_walk(c, d, int(len(ori) / window))
        temp = []
        for s in path:
            temp += list(generated[s])
        graph_res.append(temp)
    return graph_res

def Graph_update(ori, generated, window, nTS):
    used = 0
    graph_res = []
    graph_output = {}
    start = time.time()
    a, b, c, d = transform(np.array(generated), 100, 5)
    for i in tqdm(range(nTS)):
        currentTS = i
        path = random_walk(c, d, int(len(ori) / window))
        temp = []
        for s in path:
            temp += list(generated[s])
            used += 1
        graph_res.append(temp)
        if used > len(generated) * percentage_reconst // 100:
            used = 0
            graph_output[currentTS] = time.time() - start
            print(graph_output)
            print('graph reconstruction...')
            a, b, c, d = transform(np.array(generated), 100, 5)
    return graph_res, graph_output

long_seg = (4 * segments)[:10000]

lsh_const = {}
graph_const = {}
for nSeg in tqdm(range(100, 1000 + 1, 100)):
    segments = long_seg[:nSeg]
    start = time.time()
    lsh = lshash.LSHash(window // 300, 3072, num_hashtables=8)
    for i in segments:
        lsh.index(i)
    lsh_const[nSeg] = time.time() - start
    start = time.time()
    a, b, c, d = transform(np.array(segments), 100, 5)
    graph_const[nSeg] = time.time() - start

# Plot I
plt.figure()
df_const = pd.DataFrame([lsh_const, graph_const]).T
df_const.columns = ['LSH', 'Graph']
df_const.plot()
plt.title('Experiment I: Construction Runtime')
plt.xlabel('Seed Data Size')
plt.ylabel('Runtime (s)')
plt.legend(['LSH', 'Graph'])
plt.savefig('../../results/generation/experiment_I.png')
plt.close()
df_const.to_csv('../../results/experiment1_construction_runtime.csv')

lsh_input = {}
graph_input = {}
for nSeg in tqdm(range(1000, 10000 + 1, 1000)):
    segments = long_seg[:nSeg]
    start = time.time()
    lsh_res, _ = LSH_update(data, segments, window, nTS=10)
    lsh_input[nSeg] = time.time() - start
    start = time.time()
    graph_res, _ = Graph_update(data, segments, window, nTS=10)
    graph_input[nSeg] = time.time() - start

# Plot II
plt.figure()
df_input = pd.DataFrame([lsh_input, graph_input]).T
df_input.columns = ['LSH', 'Graph']
df_input.plot()
plt.title('Experiment II: Input Segments Runtime')
plt.xlabel('Data Size')
plt.ylabel('Runtime (s)')
plt.legend(['LSH', 'Graph'])
plt.savefig('../../results/generation/experiment_II.png')
plt.close()
df_input.to_csv('../../results/experiment2_input_segments_runtime.csv')

print(lsh_input, graph_input)

nTS = 1000

lsh_res, lsh_output = LSH_update(data, long_seg, window, nTS=nTS, num_hashtables=3, n_top=1)
print(lsh_output)

graph_res, graph_output = Graph_update(data, long_seg, window, nTS=nTS)
print(graph_output)

print(lsh_output, graph_output)
