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
from utils.library import *


import pymonetdb

# Generate Random Values
random.seed(1)
set_st = [str(random.randint(0,9)) for i in range(500)]
set_s = [str(random.randint(0,99)) for i in range(500)]
set_date = [random.random() for i in range(500)]

with open("../scenarios.json") as file:
	scenarios = json.load(file)

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
parser.add_argument('--n_it', nargs = '?', type = int, help = 'Minimum number of iterations', default = default_n_iter)
parser.add_argument('--timeout', nargs = '?', type = float, help = 'Query execution timeout in seconds', default = default_timeout)
parser.add_argument('--additional_arguments', nargs = '?', type = str, help = 'Additional arguments to be passed to the scripts', default = '')

def run_query(query, rangeL , rangeUnit, n_st , n_s , n_it,host="localhost"):
	# Connect to the system
	#print("query intput:", query)

	if rangeUnit in ["week","w","WEEK"]:
		rangeUnit = "day"
		rangeL = rangeL*7
	
	conn = pymonetdb.connect(username="monetdb", port=54320, password="monetdb", hostname=host, database="mydb")
	cursor = conn.cursor()	 
	runtimes = []
	full_time = time.time()
	for it in tqdm(range(n_it)):
		date = random_date("2019-04-01T00:00:00", "2019-04-30T00:00:00", set_date[(int(rangeL)*it)%500], dform = '%Y-%m-%dT%H:%M:%S')
		temp = query.replace("<timestamp>", date)
		temp = temp.replace("<range>", str(rangeL))
		temp = temp.replace("<rangesUnit>", rangeUnit)
		
		# stations
		li = ['st' + str(z) for z in random.sample(range(10), n_st)]
		q = "(" + "'" + li[0] + "'"
		for j in li[1:]:
			q += ', ' + "'" + j + "'"
		q += ")"
	
		temp = temp.replace("<stid>", q)		
		temp = temp.replace("<stid1>", f"{random.randint(1,10)}")
		temp = temp.replace("<stid2>", f"{random.randint(1,10)}") 
	
		# sensors
		li = ['s' + str(z) for z in random.sample(range(100), n_s)]
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
		



		import re 
		#match a=(b,c,...) make it a=b or a=c or ...
		equality_missmatches = re.findall(r"\b\w+\s*=\s*\([^)]*?,[^)]*?\)",temp)
		for equality_missmatch in  equality_missmatches:
			pattern , options = equality_missmatch.split("=")
			options = options.replace(")","").replace("(","").split(",")    
			res = "(" +  " or ".join( [ pattern+"= "+o  for o in options ]) +  ")"   
			temp = temp.replace(equality_missmatch,res)
		
		start = time.time()
		cursor.execute(temp)
		results_ = cursor.fetchall()

		diff = (time.time()-start)*1000
		runtimes.append(diff)
		if time.time() - full_time > 200 and it > 5: 
			break  
			
	conn.close()
	return stats.mean(runtimes), stats.stdev(runtimes)




if __name__ == "__main__":
	print('launching system monetdb')

	import os
	import subprocess
	from subprocess import Popen, PIPE, STDOUT, DEVNULL # py3k

	process = Popen(['sh', 'launch.sh', '&'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
	stdout, stderr = process.communicate()

	process = Popen(['sleep', '2'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
	stdout, stderr = process.communicate()
	
	args = parser.parse_args()

	def query_f(query, rangeL = args.range, rangeUnit = args.rangeUnit, n_st = args.def_st, n_s = args.def_s, n_it = args.n_it):
		return run_query(query, rangeL=rangeL, rangeUnit = rangeUnit ,n_st = n_st , n_s = n_s , n_it = n_it)

	run_system(args,"monetdb",query_f)


	process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
	stdout, stderr = process.communicate()

