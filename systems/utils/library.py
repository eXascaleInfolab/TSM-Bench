from datetime import datetime
from tqdm import tqdm
import os
import time
import statistics as stats
import numpy as np
import random
import json
import pandas as pd


def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.
    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop, dform='%Y-%m-%dT%H:%M:%S'):
    return str_time_prop(start, end, dform, prop)


def get_list(elm, n_elm, max_r=10, prefix='', suffix='', apostrophe=True):
    res = ''
    elms = random.sample(range(max_r), n_elm)
    for i in range(n_elm):
        item = prefix + elm + str(elms[i]) + suffix
        if apostrophe:
            item = "'" + item + "'"
        res += item
        if i < n_elm - 1:
            res += ", "
    return


def to_pm(v):
    return str(int(v[0][0])) + "$" + '\\' + "pm$" + str(int(v[1][0]))


def get_randomized_inputs(dataset, *, n_st, n_s, n_it, rangeL, seed=1):
    random.seed(seed)

    path_to_data_folder = "../../datasets" if os.path.isdir("../../datasets") else "datasets"
    with open(f"{path_to_data_folder}/dataset_config.json") as f:
        dataset_config = json.load(f)[dataset]

    n_sensors_total = dataset_config["n_sensors"]
    n_stations_total = dataset_config["n_stations"]
    time_start, time_stop = dataset_config["time_start_stop"]

    random_stations = [['st' + str(z) for z in random.sample(range(n_stations_total), n_st)] for i in range(n_it)]
    random_sensors = [['s' + str(z) for z in random.sample(range(n_sensors_total), n_s)] for i in range(n_it)]

    set_date = [random.random() for i in range(500)]

    random_dates = [random_date(time_start, time_stop, set_date[(int(rangeL) * i) % 500],
                                dform='%Y-%m-%dT%H:%M:%S') for i in range(n_it)]

    return {"stations": random_stations, "sensors": random_sensors, "dates": random_dates}
# def get_start_and_stop_dates(dataset_name):
#     # extracts the first and last line from a dataset using bash
#     import subprocess
#
#     path_to_data_folder = "../../datasets" if os.path.isdir("../../datasets") else "datasets"
#
#     #print(os.listdir(path_to_data_folder))
#
#     data_set_path =  f"{path_to_data_folder}/{dataset_name}.csv"
#
#     ##infer start date
#     command = f'head -n 2 {data_set_path} | tail -n 1'
#     head_process = subprocess.Popen(command , shell=True ,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout, stderr = head_process.communicate()
#     start_date , station , *sensors = stdout.decode("utf-8").strip().split(",")
#     start_date_pd = pd.to_datetime(start_date)
#
#     ## infer last date
#     tail_process = subprocess.Popen(['tail', data_set_path, '-n', '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout, stderr = tail_process.communicate()
#     last_date , station , *sensors = stdout.decode("utf-8").strip().split(",")
#     last_date_pd = pd.to_datetime(last_date)
#
#     return str(start_date_pd) , str(last_date_pd)
