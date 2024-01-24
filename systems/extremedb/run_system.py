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

import os
import subprocess

# setting path
sys.path.append('../../')
from systems.utils.library import *
from systems.utils import change_directory, parse_args, connection_class
from utils.run_systems import run_system

import exdb


def get_connection(host="localhost", dataset=None, **kwargs):
    load_env_variables()
    exdb.init_runtime(debug=False, shm=False, disk=False, tmgr='mursiw')
    conn = exdb.connect(host, 5001)
    cursor = conn.cursor()

    def execute_query_f(sql):
        print(sql[:600])
        cursor.execute(sql)
        return cursor.fetchall()

    def write_points_f(sql, dataset=dataset):
        cursor.execute("set append_mode true")
        cursor.execute(sql)
        return cursor.fetchall()

    conn_close_f = lambda: conn.close()
    return connection_class.Connection(conn_close_f, execute_query_f, write_points_f)


def parse_query(query, *, date, rangeUnit, rangeL, sensor_list, station_list):
    # query : query_template containing places holders
    # date : date of the query
    # rangeUnit : unit of the range
    # rangeL : length of the range (mostly 1)
    # sensor_list : list of sensors e.g [s1,s2,s2]
    # station_list : list of stations e.g [st1,st2,st3]

    options = {"day": 60 * 60 * 24,
               "week": 60 * 60 * 24 * 7,
               "minute": 60,
               "hour": 60 * 60,
               "second": 1,
               "month": 60 * 60 * 24 * 30,
               "year": 60 * 60 * 24 * 30 * 12
               }

    date = int(time.mktime(datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').timetuple()))
    temp = query.replace("<timestamp>", str(date))
    temp = temp.replace("<range>", str(rangeL))
    temp = temp.replace("<rangesUnit>", str(options[rangeUnit]))

    # stations
    q = "(" + "'" + station_list[0] + "'"
    for j in station_list[1:]:
        q += ', ' + "'" + j + "'"
    q += ")"
    temp = temp.replace("<stid>", q)

    # sensors

    sidlist = sensor_list[0]
    for j in sensor_list[1:]:
        sidlist += ',' + j
    li = [z + "@tt" for z in sensor_list]
    li_filtered = [str(z) + "@fe as " + str(z) for z in sensor_list]

    q = li[0]
    q_filtered = li_filtered[0]
    q_seq_group_agg_avg = "seq_group_agg_avg(" + li[0] + " , t@tt/3600) as " + li[0].split('@')[0]
    q_seq_avg = "seq_avg(" + li[0] + ")"
    q_seq_stretch = "seq_stretch(ts5,t," + li[0].split('@')[0] + ")"
    q_filter = "!seq_filter_search(" + li[0] + "> 0.95"
    q_filterAND = "!seq_filter_search(" + li[0] + "> 0.95"

    for j in range(1, len(li_filtered)):
        q_filtered += ', ' + li_filtered[j]

    for j in li[1:]:
        q += ', ' + j
        q_seq_avg += ", seq_avg(" + j + ")"
        q_seq_group_agg_avg += ", seq_group_agg_avg(" + j + " , t@tt/3600)" + " as " + j.split('@')[
            0]  # li[0] + ' > 0.95'
        q_seq_stretch += ", seq_stretch(ts5,t," + j.split('@')[0] + ")"
    temp = temp.replace("<sid>", q)
    temp = temp.replace("<sid1>", sensor_list[0])
    sid2 = sensor_list[1] if len(sensor_list) > 1 else "s2"
    sid3 = sensor_list[2] if len(sensor_list) > 2 else "s3"
    temp = temp.replace("<sid2>", sid2)
    temp = temp.replace("<sid3>", sid3)
    temp = temp.replace("<sidlist>", sidlist)
    temp = temp.replace("<seq_avg>", q_seq_avg)
    temp = temp.replace("<sid_filtered>", q_filtered)
    temp = temp.replace("<seq_group_agg_avg>", q_seq_group_agg_avg)
    temp = temp.replace("<sfilter>", q_filter + ", tt)")
    temp = temp.replace("<sfilterAND>", q_filterAND + ", tt)")
    temp = temp.replace("<seq_stretch>", q_seq_stretch)
    print(temp)
    return temp


def run_query(query, rangeL, rangeUnit, n_st, n_s, n_it, dataset, host="localhost"):
    # Connect to the system
    exdb.init_runtime(debug=False, shm=False, disk=False, tmgr='mursiw')
    conn = exdb.connect(host, 5001)
    cursor = conn.cursor()
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

        cursor.execute(query)
        results_ = cursor.fetchall()
        diff = (time.time() - start) * 1000

        #  print(temp, diff)
        runtimes.append(diff)
        if time.time() - full_time > 500 and it > 5:
            break

    conn.close()
    return stats.mean(runtimes), stats.stdev(runtimes)


main_process = None


def load_env_variables():
    """
    current="$(pwd)"
    echo "MCO_ROOT=$current"
    echo "MCO_LIBRARY_PATH=$current/eXtremeDB/target/bin.so"
    echo "LD_LIBRARY_PATH=$current/eXtremeDB/target/bin.so"
    """
    os.environ["MCO_ROOT"] = "systems/extremedb"
    os.environ["MCO_LIBRARY_PATH"] = "systems/extremedb/eXtremeDB/target/bin.so"
    os.environ["LD_LIBRARY_PATH"] = "systems/extremedb/eXtremeDB/target/bin.so"



def launch():
    global main_process
    print('launching system extremedb')
    with change_directory(__file__):
        # first load envioerment variables
        command = '/bin/bash -c "source variables.sh; env"'
        # Run the command as a subprocess, capturing the output
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output, error = proc.communicate()

        # Parse the output to extract the environment variables
        env_lines = [line.decode("utf-8").split('=', 1) for line in output.splitlines() if b'=' in line]
        env = dict(env_lines)
        print(f"variables to be added to venv {env}")
        # Merge the extracted environment variables with the current environment
        new_env = os.environ.copy()
        new_env.update(env)

        new_env["OLDPWD"] = os.getcwd()
        os.environ.update(new_env)

        main_process = subprocess.Popen(['sh', 'launch.sh'], env=new_env, stdin=subprocess.PIPE,
                                        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        process = subprocess.Popen(['sleep', '10'], env=new_env, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.STDOUT)
        process.communicate()


def stop():
    global main_process
    main_process.communicate()


if __name__ == "__main__":
    launch()

    args = parse_args()


    def query_f(query, rangeL=args.range, rangeUnit=args.rangeUnit, n_st=args.def_st, n_s=args.def_s, n_it=args.n_it):
        return run_query(query, rangeL=rangeL, rangeUnit=rangeUnit, n_st=n_st, n_s=n_s, n_it=n_it)


    run_system(args, "extremedb", query_f)

    stop()
