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
from library import *
import exdb

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

# # Parse Arguments
# parser = argparse.ArgumentParser(description = 'Script for running any eval')
# parser.add_argument('--system', nargs = '*', type = str, help = 'System name', default = 'clickhouse')
# parser.add_argument('--datasets', nargs = '*', type = str, help = 'Dataset name', default = 'd1')
# parser.add_argument('--queries', nargs = '?', type = str, help = 'List of queries to run (Q1-Q7)', default = ['q' + str(i) for i in range(1,8)])
# parser.add_argument('--nb_st', nargs = '?', type = int, help = 'Number of stations in the dataset', default = 10)
# parser.add_argument('--nb_s', nargs = '?', type = int, help = 'Number of sensors in the dataset', default = 100)
# parser.add_argument('--def_st', nargs = '?', type = int, help = 'Default number of queried stations', default = 1)
# parser.add_argument('--def_s', nargs = '?', type = int, help = 'Default number of queried sensors', default = 3)
# parser.add_argument('--range', nargs = '?', type = int, help = 'Query range', default = 1)
# parser.add_argument('--rangeUnit', nargs = '?', type = str, help = 'Query range unit', default = 'day')
# parser.add_argument('--max_ts', nargs = '?', type = str, help = 'Maximum query timestamp', default = "2019-04-30T00:00:00")
# parser.add_argument('--min_ts', nargs = '?', type = str, help = 'Minimum query timestamp', default = "2019-04-01T00:00:00")
# parser.add_argument('--n_it', nargs = '?', type = int, help = 'Minimum number of iterations', default = default_n_iter)
# parser.add_argument('--timeout', nargs = '?', type = float, help = 'Query execution timeout in seconds', default = default_timeout)
# parser.add_argument('--additional_arguments', nargs = '?', type = str, help = 'Additional arguments to be passed to the scripts', default = '')



def run_query(query, rangeL , rangeUnit, n_st , n_s , n_it, host="localhost"):
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
	conn = exdb.connect(host, 5001)
	cursor = conn.cursor()
	runtimes = []
	full_time = time.time()
	for it in tqdm(range(n_it)):
		date = random_date("2019-04-01T00:00:00", "2019-04-30T00:00:00", set_date[(int(rangeL)*it)%500], dform = '%Y-%m-%dT%H:%M:%S')
		date = int(time.mktime(datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').timetuple()))
		temp = query.replace("<timestamp>", str(date))
		temp = temp.replace("<range>", str(rangeL))
		temp = temp.replace("<rangesUnit>", str(options[rangeUnit]))
		
		# stations
		li = ['st' + str(z) for z in random.sample(range(10), n_st)]
		q = "(" + "'" + li[0] + "'"
		for j in li[1:]:
			q += ', ' + "'" + j + "'"
		q += ")"
		temp = temp.replace("<stid>", q)
	
		# sensors
	
		rand = [str(z) for z in random.sample(range(100), n_s)]
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
		#print(temp)
		cursor.execute(temp)
		results_ = cursor.fetchall()
		#print(results_)
		diff = (time.time()-start)*1000
		#  print(temp, diff)
		runtimes.append(diff)
		if time.time() - full_time > 500 and it > 5: 
			break  
			
	conn.close()
	return stats.mean(runtimes), stats.stdev(runtimes)

if __name__ == "__main__":
	print('launching system extremdb')

	import os
	import subprocess

	# Command to source the script and print the environment
	command = '/bin/bash -c "source variables.sh; env"'

	# Run the command as a subprocess, capturing the output
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	output, error = proc.communicate()

	# Parse the output to extract the environment variables
	env_lines = [line.decode("utf-8").split('=', 1) for line in output.splitlines() if b'=' in line]
	env = dict(env_lines)


	# Merge the extracted environment variables with the current environment
	new_env = os.environ.copy()
	new_env.update(env)

	new_env["OLDPWD"] = os.getcwd()
	os.environ.update(new_env)


	# Run launch.sh with the modified environment and let it run in the background
	process = subprocess.Popen(['sh', 'launch.sh'], env=new_env, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


	process = subprocess.Popen(['sleep', '10'], env=new_env, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	process.communicate()
    
	args = init_parser() 


	def query_f(query, rangeL = args.range, rangeUnit = args.rangeUnit, n_st = args.def_st, n_s = args.def_s, n_it = args.n_it, host="localhost"):
		return run_query(query, rangeL=rangeL, rangeUnit = rangeUnit ,n_st = n_st , n_s = n_s , n_it = n_it,host=host)
	
	run_system(args,"extremedb",query_f)
	
	
	process = subprocess.Popen(['sh', 'stop.sh'], stdin=subprocess.PIPE)
	stdout, stderr = process.communicate()



