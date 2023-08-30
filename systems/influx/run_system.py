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
sys.path.append('../')
from library import random_date

print('launching system')

import os
import subprocess
from subprocess import Popen, PIPE, STDOUT, DEVNULL # py3k

script_dir = os.path.dirname(os.path.abspath(__file__))

# Get the absolute path of the 'systems' directory (one level above)
systems_dir = os.path.join(script_dir, '..', 'systems')
sys.path.append(systems_dir)

from utils import *
from library import *

process = Popen(['sh', 'launch.sh', '&'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
stdout, stderr = process.communicate()

process = Popen(['sleep', '2'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
stdout, stderr = process.communicate()

from influxdb import InfluxDBClient

# Generate Random Values
random.seed(1)
set_st = [str(random.randint(0,9)) for i in range(500)]
set_s = [str(random.randint(0,99)) for i in range(500)]
set_date = [random.random() for i in range(500)]

with open("../scenarios.json") as file:
	scenarios = json.load(file)
	print(scenarios)

n_stations , n_sensors , n_time_ranges = scenarios["stations"],  scenarios["sensors"], scenarios["time_ranges"]
default_n_iter = int(scenarios["n_runs"])
default_timeout = scenarios["timeout"]


# Parse Arguments
parser = argparse.ArgumentParser(description = 'Script for running any eval')
parser.add_argument('--system', nargs = '*', type = str, help = 'System name', default = 'clickhouse')
parser.add_argument('--datasets', nargs = '*', type = str, help = 'Dataset name', default = 'd1')
parser.add_argument('--queries', nargs = '?', type = str, help = 'List of queries to run (Q1-Q7)', default = ['q' + str(i) for i in range(1,8)])
parser.add_argument('--nb_st', nargs = '?', type = int, help = 'Number of stations in the dataset', default = 10)
parser.add_argument('--nb_s', nargs = '?', type = int, help = 'Number of sensors in the dataset', default = 100)
parser.add_argument('--def_st', nargs = '?', type = int, help = 'Default number of queried stations', default = 1)
parser.add_argument('--def_s', nargs = '?', type = int, help = 'Default number of queried sensors', default = 3)
parser.add_argument('--range', nargs = '?', type = int, help = 'Query range', default = 1)
parser.add_argument('--rangeUnit', nargs = '?', type = str, help = 'Query range unit', default = 'day')
parser.add_argument('--max_ts', nargs = '?', type = str, help = 'Maximum query timestamp', default = "2019-04-30T00:00:00")
parser.add_argument('--min_ts', nargs = '?', type = str, help = 'Minimum query timestamp', default = "2019-04-01T00:00:00")
parser.add_argument('--n_it', nargs = '?', type = int, help = 'Minimum number of iterations', default = default_n_iter	)
parser.add_argument('--timeout', nargs = '?', type = float, help = 'Query execution timeout in seconds', default = default_timeout)
parser.add_argument('--additional_arguments', nargs = '?', type = str, help = 'Additional arguments to be passed to the scripts', default = '')
args = parser.parse_args()




def run_query(query, rangeL = args.range, rangeUnit = args.rangeUnit, n_st = args.def_st, n_s = args.def_s, n_it = args.n_it):
	# Connect to the system
	client = InfluxDBClient(host="localhost", port=8086, username='luca')
	
	runtimes = []
	n_queries = []
	full_time = time.time()
	for it in tqdm(range(n_it)):
		date = random_date(args.min_ts, args.max_ts, set_date[(int(rangeL)*it)%500], dform = '%Y-%m-%dT%H:%M:%S')
		temp = query.replace("<timestamp>", date)
		temp = temp.replace("<range>", str(rangeL))
		temp = temp.replace("<rangesUnit>", str(args.rangeUnit[0]))
		
		# stations
		li = ['st' + str(z) for z in random.sample(range(args.nb_st), n_st)]
		#  print(li)
		q = '(id_station =' + "'" + li[0] + "'"
		for j in li[1:]:
			q += ' OR '  + 'id_station =' + "'" + j + "'"
		q += ")"
		temp = temp.replace("<stid>", q)
	
		# sensors
		li = ['s' + str(z) for z in random.sample(range(args.nb_s), n_s)]
		q = ",".join(li)
		q_filter = "( " + li[0] + ' > 0.95' +")"
		q_avg =  ",".join([f"mean({e})" for e in li])  #'mean(' + li[0] + ')'
		q_avg_ = ",".join([f"mean_{e}" for e in li])
		q_avg_as = ",".join([ f"mean({e})  as mean_{e}" for e in li])
                
		temp = temp.replace("<sid>", q)
		temp = temp.replace("<sid1>", str(set_s[(args.range*it)%500]))
		temp = temp.replace("<sid2>", str(set_s[(args.range*(it+1))%500]))
		temp = temp.replace("<sid>", q)
		temp = temp.replace("<sfilter>", q_filter )
		temp = temp.replace("<avg_s>", q_avg)                
		temp = temp.replace("<avg_s_>", q_avg_)                
		temp = temp.replace("<avg_s_as>", q_avg_as)
		
		start = time.time()
		queries = client.query(temp)
		diff = (time.time()-start)*1000

		runtimes.append(diff)
		if time.time() - full_time > args.timeout and it > 5: 
			break  
			
	client.close()
	return round(stats.mean(runtimes),3) , round(stats.stdev(runtimes),3)


run_system(args,"influx",run_query)

process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
stdout, stderr = process.communicate()

