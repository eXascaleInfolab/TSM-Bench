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
from subprocess import Popen, PIPE, STDOUT, DEVNULL # py3k

# setting path
sys.path.append('../../')
from systems.utils.library import *
from systems.utils import change_directory , parse_args
from utils.run_systems import run_system


import psycopg2

def parse_query(query ,*, date, rangeUnit , rangeL , sensor_list , station_list):
    temp = query.replace("<timestamp>", date)
    temp = temp.replace("<range>", str(rangeL))
    temp = temp.replace("<rangesUnit>", rangeUnit)

    # stations
    q = "(" + "'" + station_list[0] + "'"
    for j in station_list[1:]:
        q += ', ' + "'" + j + "'"
    q += ")"
    temp = temp.replace("<stid>", q)

    # sensors
    q = sensor_list[0]
    q_filter = '(' + sensor_list[0] + ' > 0.95'
    q_avg = 'avg(' + sensor_list[0] + ')'
    q_interpolate_avg = 'interpolate(avg(' + sensor_list[0] + '))'
    for j in sensor_list[1:]:
        q += ', ' + j
        # q_filter += ' OR ' + j + ' > 0.95'
        q_avg += ', ' + 'avg(' + j + ')'
        q_interpolate_avg += ', interpolate(avg(' + j + '))'

    temp = temp.replace("<sid>", q)
    temp = temp.replace("<sid1>", sensor_list[0] )
    sid2 = sensor_list[1] if len(sensor_list) > 1 else "s2"
    sid3 = sensor_list[2] if len(sensor_list) > 2 else "s3"
    temp = temp.replace("<sid2>", sid2)
    temp = temp.replace("<sid3>", sid3)
    temp = temp.replace("<interpolate_avg>", q_interpolate_avg)
    temp = temp.replace("<sfilter>", q_filter + ')')
    temp = temp.replace("<avg_s>", q_avg)

    return temp

def run_query(query, rangeL , rangeUnit , n_st , n_s , n_it, dataset , host="localhost"):
    # Connect to the system
    CONNECTION = f"postgres://postgres:postgres@{host}:5432/postgres"
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()


    if rangeUnit in ["week","w","Week"]:
        rangeUnit = "day"
        rangleL = rangeL*7

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
        # print(temp)
        cursor.execute(query)
        results_ = cursor.fetchall()

        diff = (time.time()-start)*1000
        #  print(temp, diff)
        runtimes.append(diff)
        if time.time() - full_time > 100 and it > 5: 
            break  

    conn.close()
    return stats.mean(runtimes), stats.stdev(runtimes)



def launch():
    
    print("launching timescaledb")

    with change_directory(__file__):
        process = Popen(['sh', 'variables.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

        process = Popen(['sh', 'launch.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

        process = Popen(['sleep', '10'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

def stop():
   
    with change_directory(__file__):
        process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

        

db_name = "timescaledb"
if __name__ == "__main__":
    
    args =parse_args() 

    launch()

    def query_f(query, rangeL = args.range, rangeUnit = args.rangeUnit, n_st = args.def_st, n_s = args.def_s, n_it = args.n_it):
                return run_query(query, rangeL = rangeL, rangeUnit = rangeUnit, n_st = n_st, n_s = n_s, n_it = n_it)

    run_system(args,"timescaledb",query_f)
    
    stop()
