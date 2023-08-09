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

# setting path
sys.path.append('../')
from library import *

print('launching system')

import os
import subprocess
from subprocess import Popen, PIPE, STDOUT, DEVNULL # py3k

process = Popen(['sh', 'variables.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
stdout, stderr = process.communicate()

process = Popen(['sh', 'launch.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
stdout, stderr = process.communicate()

process = Popen(['sleep', '3'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
stdout, stderr = process.communicate()

import exdb 

# Generate Random Values
random.seed(1)
set_st = [str(random.randint(0,9)) for i in range(500)]
set_s = [str(random.randint(0,99)) for i in range(500)]
set_date = [random.random() for i in range(500)]


# Parse Arguments
parser = argparse.ArgumentParser(description = 'Script for running any eval')
parser.add_argument('--system', nargs = '*', type = str, help = 'System name', default = 'clickhouse')
parser.add_argument('--datasets', nargs = '*', type = str, help = 'Dataset name', default = 'd1')
parser.add_argument('--queries', nargs = '*', type = str, help = 'List of queries to run (Q1-Q7)', default = ['q' + str(i) for i in range(1,8)])
parser.add_argument('--nb_st', nargs = '?', type = int, help = 'Number of stations in the dataset', default = 10)
parser.add_argument('--nb_s', nargs = '?', type = int, help = 'Number of sensors in the dataset', default = 100)
parser.add_argument('--def_st', nargs = '?', type = int, help = 'Default number of queried stations', default = 1)
parser.add_argument('--def_s', nargs = '?', type = int, help = 'Default number of queried sensors', default = 3)
parser.add_argument('--range', nargs = '?', type = int, help = 'Query range', default = 1)
parser.add_argument('--rangeUnit', nargs = '?', type = str, help = 'Query range unit', default = 'day')
parser.add_argument('--max_ts', nargs = '?', type = str, help = 'Maximum query timestamp', default = "2019-04-30T00:00:00")
parser.add_argument('--min_ts', nargs = '?', type = str, help = 'Minimum query timestamp', default = "2019-04-01T00:00:00")
parser.add_argument('--n_it', nargs = '?', type = int, help = 'Minimum number of iterations', default = 100)
parser.add_argument('--timeout', nargs = '?', type = float, help = 'Query execution timeout in seconds', default = 20)
parser.add_argument('--additional_arguments', nargs = '?', type = str, help = 'Additional arguments to be passed to the scripts', default = '')
args = parser.parse_args()



def run_query(query, rangeL = args.range, rangeUnit = args.rangeUnit, n_st = args.def_st, n_s = args.def_s, n_it = args.n_it):
	options = {"day" : 60 * 60* 24,
			   "week" : 60 * 60* 24 * 7,
			   "minute" : 60,
			   "hour" : 60 * 60,
			   "second" : 1,
			   "month" : 60 * 60 * 24 * 30,
			   "year" :  60 * 60 * 24 * 30 * 12
	}	
	# Connect to the system
	exdb.init_runtime(debug = False, shm = False, disk = False, tmgr = 'mursiw')
	conn = exdb.connect('localhost', 5001)
	cursor = conn.cursor()
	runtimes = []
	full_time = time.time()
	for it in tqdm(range(n_it)):
		date = random_date(args.min_ts, args.max_ts, set_date[(int(rangeL)*it)%500], dform = '%Y-%m-%dT%H:%M:%S')
		date = int(time.mktime(datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').timetuple()))
		temp = query.replace("<timestamp>", str(date))
		temp = temp.replace("<range>", str(rangeL))
		temp = temp.replace("<rangesUnit>", str(options[rangeUnit]))
		
		# stations
		li = ['st' + str(z) for z in random.sample(range(args.nb_st), n_st)]
		q = "(" + "'" + li[0] + "'"
		for j in li[1:]:
			q += ', ' + "'" + j + "'"
		q += ")"
		temp = temp.replace("<stid>", q)
	
		# sensors
		rand = [str(z) for z in random.sample(range(args.nb_st), n_s)]
		sidlist = 's' + rand[0]
		for j in rand[1:]:
			sidlist += ',' + 's' +  j
		li = ['s' + str(z) + "@tt" for z in rand]
		li_filtered = ['s' + str(z) + "@fe as s" + str(z) for z in rand]
		
		q = li[0]
		q_filtered = li_filtered[0] 
		q_seq_group_agg_avg = "seq_group_agg_avg(" + li[0] + " , t@tt/3600) as " + li[0].split('@')[0]
		q_seq_avg = "seq_avg(" + li[0] + ")" 
		q_seq_stretch = "seq_stretch(ts5,t," + li[0].split('@')[0] + ")" 
		q_filter = "!seq_filter_search(" +li[0] + "> 0.95"
		q_filterAND = "!seq_filter_search(" +li[0] + "> 0.95"
		
		for j in range(1,len(li_filtered)):
			q_filtered += ', ' + li_filtered[j] 

		for j in li[1:]:
			q += ', ' + j
			q_seq_avg += ", seq_avg(" + j + ")" 
			q_seq_group_agg_avg += ", seq_group_agg_avg(" + j + " , t@tt/3600)" + " as " +  j.split('@')[0] #        li[0] + ' > 0.95'
			q_seq_stretch += ", seq_stretch(ts5,t," + j.split('@')[0] + ")" 
		temp = temp.replace("<sid>", q)
		temp = temp.replace("<sid1>", str(set_s[(rangeL*it)%500]))
		temp = temp.replace("<sid2>", str(set_s[(rangeL*(it+1))%500]))
		temp = temp.replace("<sid3>", str(set_s[(rangeL*(it+2))%500]))
		temp = temp.replace("<sidlist>", sidlist)
		temp = temp.replace("<seq_avg>", q_seq_avg)
		temp = temp.replace("<sid_filtered>", q_filtered)
		temp = temp.replace("<seq_group_agg_avg>", q_seq_group_agg_avg)
		temp = temp.replace("<sfilter>", q_filter + ", tt)")
		temp = temp.replace("<sfilterAND>", q_filterAND + ", tt)")
		temp = temp.replace("<seq_stretch>", q_seq_stretch)    
	
		
		start = time.time()
		# print(temp)
		
		cursor.execute(temp)
		cursor.fetchall()
		diff = (time.time()-start)*1000
		#  print(temp, diff)
		runtimes.append(diff)
		if time.time() - full_time > args.timeout and it > 5: 
			break  
			
	conn.close()
	return stats.mean(runtimes), stats.stdev(runtimes)


# Read Queries
with open('queries.sql') as file:
	queries = [line.rstrip() for line in file]


runtimes = []
datasets = args.datasets.split()
	# Execute queries
for dataset in datasets: 
	print(dataset)
	for query in queries: 
		if 'SELECT' in query.upper():
			query = query.replace("<db>", dataset)
			runtimes.append(run_query(query))
		else: 
			print('Query not supported.')
			runtimes.append((-1,-1))

runtimes = pd.DataFrame(runtimes, columns=['runtime','stddev'], index=['q' + str(i+1) for i in range(len(runtimes))]).astype(int)
print(runtimes)	




