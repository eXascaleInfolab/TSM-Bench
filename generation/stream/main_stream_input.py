import json
import multiprocessing
import hashing.lsh_main as lsh
# import graph.graph_main as graph
import time
from pathlib import Path
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import stream.graph.random_walk_ori as random_walk

''' 
    set code for reading generated fragments and concatenate them using: 
        - LSH
        - Graph
        - Random
        
    while computing their runtime. 
    
    go through the final generated data and compute: MI, RMSE, ED.
    
'''

with open("../parameters.json", "r") as f:
    queue_fake = multiprocessing.Queue()
    para_dict = json.load(f)
    # data_path = para_dict["input_data_path"][0]
    data_path = '/Users/abdel/PycharmProjects/TS-Benchmark/data/full_bafu.txt'
    window = para_dict["window"]
    model_path = para_dict["model_path"]  # model path
    autocorr_lag = int(para_dict["autocorr_lag"])  # model path
    # batch_size_generation = para_dict["batch_size_generation"]  # batch_size_generation
    winShift = para_dict["winShift"]
    winShift = [i for i in range(winShift[0], winShift[1], winShift[2])]
    # num_cont = para_dict["num_cont"]
    bool_train = para_dict["train"] == 1
    bool_generate = para_dict["generate"] == 1
    # bool_MP = para_dict["MP"] == 1
    bool_LSH = para_dict["lsh_conca"] == 1
    bool_metrics = para_dict["bool_metrics"] == 1
    gen_ts_length = para_dict["gen_ts_length"]
    if gen_ts_length < 2: gen_ts_length = 1
    gen_ts_dim = para_dict["gen_ts_dim"]
    nb_fragments = para_dict["nb_fragments"]
    top_n = 30
    # top_n = 0.01 * nb_fragments
    sampling_size = para_dict["sampling_size"]
    input_data_name = para_dict["input_data_name"]
    train_ep = para_dict["train_ep"]
    conca_plot = para_dict["conca_plot"] == 1
    num_hashtables = para_dict["num_hashtables"]
    hash_size_percentage = para_dict["hash_size_percentage"]
    update_percentage = para_dict["update_percentage"]

# data_path = '../' + para_dict["input_data_path"][0]
# data_path = '/Users/abdel/PycharmProjects/tsgen-backup/datasets/augmented-datasets/air_quality/airq_normal.txt'

# gen_path = '/Users/abdel/PycharmProjects/tsgen/results/airq_normal/win=384_ep=1000_nbTS=260/shift=1/model/train/'
# gen_path = '/Users/abdel/PycharmProjects/tsgen/results/GoldwindSensor/win=384_ep=100/sampling_size=7500/model/train/'
gen_path = '/Users/abdel/PycharmProjects/ABench-IoT/Generation/results/infogan_results/results/Alabama1ts/win=768_ep=300/sampling_size=100000/model/train/'
# gen_path = '../../Generation/gan/dcgan/'

# geeration_model = 0

# dataset = 'airq_normal/'

export_path = './result_stream/' + input_data_name

Path(export_path).mkdir(parents=True, exist_ok=True)

file_object = open(export_path + 'time_results.txt', 'a')
row = str('nb_fragments')

dict = {'lsh': 1,
        'graph': 1,
        'naive': 0}

if dict['lsh']: row += ',' + str('LSH_time')
if dict['graph']: row += ',' + str('Graph_time')
if dict['naive']: row += ',' + str('Naive_time')
row += '\n'

file_object.write(row)
file_object.close()

nbTS = 1

# nb_fragments = 26040

# LSH
if dict['lsh']:
    Path(export_path + 'lsh/').mkdir(parents=True, exist_ok=True)
    lsh_class = lsh.LSH_conca()
    # LSH_time = lsh_class.lsh_main(data_path, gen_path,
    #                               export_path, window, top_n,
    #                               sampling_size, conca_plot, num_hashtables, hash_size_percentage,
    #                               gen_ts_length=gen_ts_length, gen_ts_dim=gen_ts_dim)

    df_fake = pd.read_csv(gen_path + 'fake0.csv', header=None)
    df_fake = df_fake.T

    time_results = []
    for seq in range(1000, 26040, 1000):
    # for seq in range(1000, df_fake.shape[0], 1000):
        nb_fragments = seq
        LSH_time = lsh_class.lsh_main_input_complexity(data_path, df_fake[:seq],
                                                       export_path, window, top_n,
                                                       sampling_size, conca_plot, num_hashtables, hash_size_percentage,
                                                       update_percentage, nb_fragments,
                                                       gen_ts_length=gen_ts_length, gen_ts_dim=gen_ts_dim)

        file_object = open(export_path + 'time_lsh_input.txt', 'a')
        file_object.write('%s:%s\n' % ((window + seq * (winShift[0] - 1), LSH_time)))
        file_object.close()

# Graph
if dict['graph']:
    Path(export_path + 'graph/').mkdir(parents=True, exist_ok=True)
    random_walk_class = random_walk.RandomWalkOri()

    data = np.loadtxt(gen_path + 'fake0.csv', delimiter=',', encoding='utf-8-sig')  # generated data with Kalman filter
    data = data.T

    for seq in range(1000, 26040, 1000):
    # for seq in range(1000, data.shape[0], 1000):
        nb_fragments = seq
        Graph_time = random_walk_class.main(data[:seq],
                                            nb_fragments, export_path + 'graph/', gen_ts_length,
                                            update_percentage, window)

        file_object = open(export_path + 'time_graph_input.txt', 'a')
        file_object.write('%s:%s\n' % ((window + seq * (winShift[0] - 1), Graph_time)))
        file_object.close()

    # head_tail_length = 4
    # sim_thresh = 1 / 2
    # argmax = 3
    # Graph_time = graph_class.graph_main(10, gen_path,
    #                                     export_path, window, sampling_size, sim_thresh, argmax, head_tail_length,
    #                                     gen_ts_length, nb_fragments)

# Naive
if dict['naive']:
    Path(export_path + 'naive/').mkdir(parents=True, exist_ok=True)
    start_Naive = time.time()
    for i in range(nbTS):
        print(i)
        df_fake = pd.read_csv(gen_path + 'fake' + str(i) + '.csv')
        # df_fake = df_fake.T
        # print(df_fake)
        res = []
        # for j in range(int(gen_ts_length * sampling_size / window) + 1):
        for j in range(100):
            res.extend(df_fake[random.choice(df_fake.columns.values)])
        np.savetxt(export_path + "naive/fake_long" + str(i) + ".csv", np.array(res), delimiter=",")
    Naive_time = time.time() - start_Naive

row = str(nb_fragments)
if dict['lsh']: row += ',' + str(LSH_time)
if dict['graph']: row += ',' + str(Graph_time)
if dict['naive']: row += ',' + str(Naive_time)
row += '\n'

file_object = open(export_path + 'time_results.txt', 'a')
file_object.write(row)
file_object.close()
