from datetime import datetime
from tqdm import tqdm
import argparse
import os
import time
import statistics as stats
import numpy as np
import random
import sys
import pandas as pd
import json 

# setting path
sys.path.append('../../')
sys.path.append("systems")

from systems.utils.library import random_date

from systems.utils.library import *

from systems.utils import change_directory , parse_args , connection_class
from utils.run_systems import run_system

from influxdb import InfluxDBClient
from subprocess import Popen, PIPE, STDOUT, DEVNULL # py3k



def get_connection(host="localhost", dataset=None , **kwargs):
    client = InfluxDBClient(host=host, port=8086, username='name')
    def execute_query_f(sql):
        return client.query(sql)[0]


    def write_points_f(points ,dataset=dataset):
        #input: "sensor,id_station=st99 s0=<>,s1=0.256154,s2=0.353368,s3=0.264800,s4=0.340716 ....

        assert dataset is not None, "influx requires the dataset to be specified"
        return client.write_points(points, database=dataset, time_precision="ms", batch_size=5000 ,protocol='line')

    conn_close_f = lambda : client.close()
    return connection_class.Connection(conn_close_f, execute_query_f, write_points_f)


def parse_query(query ,*, date, rangeUnit , rangeL , sensor_list , station_list):
    temp = query.replace("<timestamp>", date)
    if rangeUnit == "month":
        rangeL = rangeL * 30
        rangeUnit = "day"

    temp = temp.replace("<range>", str(rangeL))
    temp = temp.replace("<rangesUnit>", str(rangeUnit[0]))
    # stations

    q = '(id_station =' + "'" + station_list[0] + "'"
    for j in station_list[1:]:
        q += ' OR ' + 'id_station =' + "'" + j + "'"
    q += ")"
    temp = temp.replace("<stid>", q)

    # sensors
    q = ",".join(sensor_list)
    q_filter = "( " + sensor_list[0] + ' > 0.95' + ")"
    q_avg = ",".join([f"mean({e})" for e in sensor_list])  # 'mean(' + li[0] + ')'
    q_avg_ = ",".join([f"mean_{e}" for e in sensor_list])
    q_avg_as = ",".join([f"mean({e})  as mean_{e}" for e in sensor_list])

    temp = temp.replace("<sid>", q)
    temp = temp.replace("<sid1>", "s1")
    temp = temp.replace("<sid2>", "s2")
    temp = temp.replace("<sid>", q)
    temp = temp.replace("<sfilter>", q_filter)
    temp = temp.replace("<avg_s>", q_avg)
    temp = temp.replace("<avg_s_>", q_avg_)
    temp = temp.replace("<avg_s_as>", q_avg_as)

    return temp

def run_query(query, rangeL , rangeUnit , n_st , n_s , n_it , dataset , host = "localhost" ):
    # Connect to the system
    client = InfluxDBClient(host=host, port=8086, username='name')
    

    random_inputs = get_randomized_inputs(dataset, n_st=n_st, n_s=n_s, n_it=n_it, rangeL=rangeL)
    random_stations = random_inputs["stations"]
    random_sensors = random_inputs["sensors"]
    random_sensors_dates = random_inputs["dates"]

    runtimes = []
    full_time = time.time()

    for it in tqdm(range(n_it)):
        date = random_sensors_dates[it]
        sensor_list = random_sensors[it]
        station_list = random_stations[it]

        assert len(sensor_list) == n_s
        assert len(station_list) == n_st
        assert type(date) == str

        query = parse_query(query, date=date, rangeUnit=rangeUnit, rangeL=rangeL, sensor_list=sensor_list,
                            station_list=station_list)

        start = time.time()
        queries = client.query(query)
        #print("done querying")
        diff = (time.time()-start)*1000
        runtimes.append(diff)
        if time.time() - full_time > 200 and it > 5: 
            break  

    client.close()
    return round(stats.mean(runtimes),3) , round(stats.stdev(runtimes),3)


def launch():
    print("launching influx")
    
    with change_directory(__file__):
        main_process = Popen(['sh', 'launch.sh' ], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        process = Popen(['sleep', '20'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

def stop():
    print("shutting down")
    command = "ps -ef | grep 'influxd' | grep -v grep | awk '{print $2}' | xargs -r kill -9"
    process = Popen(command, shell=True, stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    stdout, stderr = process.communicate()
    
    
if __name__ == "__main__":
    
    args = parse_args() 

    launch()

    def query_f(query, rangeL = args.range, rangeUnit = args.rangeUnit, n_st = args.def_st, n_s = args.def_s, n_it = args.n_it, host = "localhost"):
        return run_query(query, rangeL = rangeL, rangeUnit = rangeUnit, n_st = n_st, n_s = n_s, n_it = n_it, host= host)

    run_system(args,"influx",query_f)

    stop()


