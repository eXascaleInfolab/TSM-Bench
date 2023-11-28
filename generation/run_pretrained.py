import json
import multiprocessing
import hashing.lsh_main as lsh
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
import pandas as pd
import numpy as np
from tqdm import tqdm
import warnings
import random
warnings.filterwarnings('ignore')

import toml
config = toml.load('./config.toml')

num_hashtables = int(config['generation']['num_hashtables'])
nb_top = int(config['generation']['n_top'])
hash_length_percentage = int(config['generation']['hash_length_percentage'])

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def moving_avg(x, len_ts):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[len_ts:] - cumsum[:-len_ts]) / float(len_ts)

def TS_LSH(data, segments, nb_ts, len_ts):
    print('Building LSH...')
    lsh = lshash.LSHash(num_hashtables, window, num_hashtables=num_hashtables)

    for i in segments:
        lsh.index(segments[i])
    to_query = [data[i:i + window] for i in range(0, len(data) - window, window)]

    print('Querying LSH...')
    lsh_res = []
    n_top = nb_top
    k = int(window * hash_length_percentage / 100)

    len_ts = len_ts if len_ts > len(to_query) else len(to_query)
    for i in tqdm(range(nb_ts)):
        for _ in range(5):
            try:
                temp = list(random.choice( lsh.query(to_query[0], distance_func="euclidean", num_results=n_top))[0][0])
                break  
            except Exception as e:
                pass
        else:
            temp = list(to_query[0] + np.random.normal(0,.008, window))
        for i in range(1, len_ts // window + 2): 
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
        lsh_res.append(temp[:len_ts])    
    return lsh_res

def filter_segment(df_segments):
    print('Filtering GAN generated data...')
    len_ts = 10  # the larger len_ts is, the smoother curve will be
    b = [1.0 / len_ts] * len_ts
    a = 1
    for col in tqdm(df_segments):
        yy = lfilter(b,a,df_segments[col].tolist())
        yy[:len_ts] = yy[len_ts:len_ts+1]
        df_segments[col] = yy.tolist()
    df_segments.iloc[: , :50].plot(subplots=True, layout=(10,6), figsize=(10, 10), legend = True, color = 'b')
#     plt.show()
    
def plot_result(data, lsh_res, nb_ts, len_ts, seed):
    print('Plotting the results')
    xi = list(range(len_ts))
    plt.figure(figsize=(60, 30))
    plt.subplot(nb_ts+1, 1, 1)
    # plt.figure(figsize=(60, 8))
    plt.plot(data[:len_ts],color='blue',linewidth=4.0, label='Original')
    plt.xlim(0,len_ts)
#     plt.ylim(8.1,8.7)
    plt.legend(loc="upper left", prop={'size': 36})
    for i in range(2, nb_ts+2):
        plt.subplot(nb_ts+1, 1, i)
        plt.plot(lsh_res[i-2],color='green',linewidth=4.0)
        plt.xlim(0,len(lsh_res[0]))
#         plt.ylim(8.1,8.7)
        plt.legend(loc="upper left", prop={'size': 36})
    plt.savefig('results/' + seed + '.png', bbox_inches='tight')         

parser = argparse.ArgumentParser(description="A script that takes two integer values as input and calls a function with them.")
parser.add_argument("--len_ts", type=int, default=10000, help="Length of ts")
parser.add_argument("--nb_ts", type=int, default=3, help="Number of ts")
parser.add_argument("--seed", type=str, default='conductivity', help="Link to original dataset")
# parser.add_argument("--fsynth", type=str, default='data/column_23_3072_3072.txt', help="Link to synthetic segments")
args = parser.parse_args()

# generate_rand(fseed, fsynth)

len_ts = args.len_ts
nb_ts = args.nb_ts
seed = args.seed
fseed = 'data/' + args.seed + '/original.txt'
fsynth = 'data/' + args.seed + '/synthetic.txt'

window = 3072
# len_ts = 10000
# nb_ts = 3

try: 
    data = pd.read_csv(fseed)
    data = data.iloc[:,0].tolist()
    data = moving_avg(data, 5).tolist()
    len(data)
    df_segments = pd.read_csv(fsynth).T

    lsh_res = TS_LSH(data, df_segments, nb_ts, len_ts)

    plot_result(data, lsh_res, nb_ts, len_ts, seed)
    lsh_res = pd.DataFrame(lsh_res).T
    lsh_res.to_csv('results/'+seed+'.txt', header = False, index = False, float_format='%.3f')

    print('Generated', lsh_res.shape[1], 'time series of length', lsh_res.shape[0])
except: 
    print("Error reading file")


# data = data.iloc[:,0].tolist()
# seed = 'conductivity'
# fseed = 'data/' + seed + '/original.txt'
# fsynth = 'data/' + seed + '/synthetic.txt'

# df_segments = [df_segments.iloc[:,i] for i in range(len(df_segments)-1)]
# segments = [data[i:i + window] + np.random.normal(0,.008, window) for i in range(0, len(data) - window, int(0.1 * window))]
# df_segments = pd.DataFrame(segments)
# df_segments = df_segments.T
# # df_segments.iloc[: , :50].plot(subplots=True, layout=(10,6), figsize=(10, 10), legend = True, color = 'b')
# # plt.show()
# # df_segments = filter_segment(df_segments)
