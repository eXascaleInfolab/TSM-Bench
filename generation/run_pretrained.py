import json
import multiprocessing
import lsh_main as lsh
import time
from pathlib import Path
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import lshashpy3 as lshash
import math 
from scipy.signal import lfilter
import csv
import argparse

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def moving_avg(x, n):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[n:] - cumsum[:-n]) / float(n)

def TS_LSH(data, segments, m, n):
    print('Building LSH...')
    lsh = lshash.LSHash(8, window, num_hashtables=8)

    for i in segments:
        lsh.index(segments[i])
    to_query = [data[i:i + window] for i in range(0, len(data) - window, window)]

    print('Querying LSH...')
    lsh_res = []
    n_top = 10
    k = int(window * .03)

    n = n if n > len(to_query) else len(to_query)
    for i in tqdm(range(m)):
        for _ in range(5):
            try:
                temp = list(random.choice( lsh.query(to_query[0], distance_func="euclidean", num_results=n_top))[0][0])
                break  
            except Exception as e:
                pass
        else:
            temp = list(to_query[0] + np.random.normal(0,.008, window))
        for i in range(1, n // window + 2): 
            for _ in range(5):
                try:
                    s = list(random.choice( lsh.query(to_query[i%len(to_query)], distance_func="euclidean", num_results=n_top))[0][0])
                    break  
                except Exception as e:
                    pass
            else:
                s =list(to_query[i%len(to_query)])
            temp_t = temp[-k:]
            s_h = s[:k]
            overlap = []
            for i in range(-k//2, k//2):
                overlap.append((1 - sigmoid(i))*temp_t[i + k//2] + sigmoid(i)*s_h[i + k//2])
            temp[-k:] = overlap
            temp.extend(s[k:])
        lsh_res.append(temp[:n])    
    return lsh_res

def filter_segment(df_segments):
    print('Filtering GAN generated data...')
    n = 10  # the larger n is, the smoother curve will be
    b = [1.0 / n] * n
    a = 1
    for col in tqdm(df_segments):
        yy = lfilter(b,a,df_segments[col].tolist())
        yy[:n] = yy[n:n+1]
        df_segments[col] = yy.tolist()
    df_segments.iloc[: , :50].plot(subplots=True, layout=(10,6), figsize=(10, 10), legend = True, color = 'b')
#     plt.show()
    
def plot_result(data, lsh_res, m, n):
    print('Plotting the results')
    xi = list(range(n))
    plt.figure(figsize=(60, 30))
    plt.subplot(m+1, 1, 1)
    # plt.figure(figsize=(60, 8))
    plt.plot(data[:n],color='blue',linewidth=4.0, label='Original')
    plt.xlim(0,n)
#     plt.ylim(8.1,8.7)
    plt.legend(loc="upper left", prop={'size': 36})
    for i in range(2, m+2):
        plt.subplot(m+1, 1, i)
        plt.plot(lsh_res[i-2],color='green',linewidth=4.0, label='LSH')
        plt.xlim(0,len(lsh_res[0]))
#         plt.ylim(8.1,8.7)
        plt.legend(loc="upper left", prop={'size': 36})



parser = argparse.ArgumentParser(description="A script that takes two integer values as input and calls a function with them.")
parser.add_argument("--n", type=int, default=10000, help="Length of ts")
parser.add_argument("--m", type=int, default=3, help="Number of ts")
parser.add_argument("--fori", type=str, default='data/sample_dataset.csv', help="Link to original dataset")
parser.add_argument("--fsynth", type=str, default='data/column_23_3072_3072.txt', help="Link to synthetic segments")
parser.add_argument("--output_to", type=str, default='results/lsh.csv', help="Link to result file")
args = parser.parse_args()
n = args.n
m = args.m
fori = args.fori
fsynth = args.fsynth
output_to = args.output_to

window = 3072

data = pd.read_csv(fori)
data = data.iloc[:,7].tolist()
# data = data.iloc[:,0].tolist()

data = moving_avg(data, 200).tolist()
len(data)

df_segments = pd.read_csv(fsynth).T

# df_segments = [df_segments.iloc[:,i] for i in range(len(df_segments)-1)]
# segments = [data[i:i + window] + np.random.normal(0,.008, window) for i in range(0, len(data) - window, int(0.1 * window))]
# df_segments = pd.DataFrame(segments)
# df_segments = df_segments.T
# # df_segments.iloc[: , :50].plot(subplots=True, layout=(10,6), figsize=(10, 10), legend = True, color = 'b')
# # plt.show()
# # df_segments = filter_segment(df_segments)

lsh_res = TS_LSH(data, df_segments, m, n)

plot_result(data, lsh_res, m, n)
lsh_res = pd.DataFrame(lsh_res).T
lsh_res.to_csv(output_to, header = False, index = False, float_format='%.6f')

print('Generated', lsh_res.shape[1], 'time series of length', lsh_res.shape[0])


