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

import subprocess
from subprocess import Popen, PIPE, STDOUT, DEVNULL

from pydruid.client import *
from pydruid.db import connect
from pydruid.utils.aggregators import *
from pydruid.utils.filters import *

# setting path
sys.path.append('../../')
from systems.utils.library import *
from systems.utils import change_directory , parse_args
from systems import run_system


# Generate Random Values
random.seed(1)
set_st = [str(random.randint(0,9)) for i in range(500)]
set_s = [str(random.randint(0,99)) for i in range(500)]
set_date = [random.random() for i in range(500)]

def run_query(query, rangeL ,rangeUnit ,n_st ,n_s ,n_it , host="localhost"):

    if rangeUnit in ["week","w","Week"]:
        rangeUnit = "day"
        rangeL = rangeL*7

    # Connect to the system
    conn = connect(host='localhost', port=8082, path='/druid/v2/sql/', scheme='http')	
    cursor = conn.cursor()
    runtimes = []
    full_time = time.time()
    for it in tqdm(range(n_it)):
        date = random_date(args.min_ts, args.max_ts, set_date[(int(rangeL)*it)%500], dform = '%Y-%m-%d %H:%M:%S')
        temp = query.replace("<timestamp>", date)
        temp = temp.replace("<range>", str(rangeL))
        temp = temp.replace("<rangesUnit>", rangeUnit)
        
        # stations
        li = ['st' + str(z) for z in random.sample(range(args.nb_st), n_st)]
        q = "(" + "'" + li[0] + "'"
        for j in li[1:]:
            q += ', ' + "'" + j + "'"
        q += ")"
        temp = temp.replace("<stid>", q)

        # sensors
        li = ['s' + str(z) for z in random.sample(range(args.nb_s), n_s)]
        q = li[0]
        q_filter = '(' + li[0] + ' > 0.95'
        q_avg = 'avg(' + li[0] + ')'
        for j in li[1:]:
            q += ', ' + j
            # q_filter += ' OR ' + j + ' > 0.95'
            q_avg += ', ' + 'avg(' + j + ')'
        temp = temp.replace("<sid>", q)
        temp = temp.replace("<sid1>", str(set_s[(rangeL*it)%500]))
        temp = temp.replace("<sid2>", str(set_s[(rangeL*(it+1))%500]))
        temp = temp.replace("<sid3>", str(set_s[(rangeL*(it+2))%500]))
        temp = temp.replace("<sfilter>", q_filter + ')')
        temp = temp.replace("<avg_s>", q_avg)

        start = time.time()
        
        cursor.execute(temp)
        results_ = cursor.fetchall()
        diff = (time.time()-start)*1000
        #  print(temp, diff)
        runtimes.append(diff)
        if time.time() - full_time > args.timeout and it > 5: 
            break  
            
    conn.close()
    return stats.mean(runtimes), stats.stdev(runtimes)


def launch():
    
    print("launching druid")

    with change_directory(__file__):
        process = Popen(['sh', 'launch.sh', '&'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate() #launch.sh  from druid has to sleep for long itself
    
    print("druid launched")
    
def stop():
   
    with change_directory(__file__):
        process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

    
if __name__ == "__main__":
    
    launch()
    
    args = parse_args() 
    
    def query_f(query, rangeL = args.range, rangeUnit = args.rangeUnit, n_st = args.def_st, n_s = args.def_s, n_it = args.n_it):
        return run_query(query, rangeL=rangeL, rangeUnit = rangeUnit ,n_st = n_st , n_s = n_s , n_it = n_it)
    
    run_system(args,"clickhouse",query_f)

    stop()
    
  