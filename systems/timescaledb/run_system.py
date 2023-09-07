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

import psycopg2

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
show_loading_bar = scenarios["loadingbar"]

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
parser.add_argument('--online', nargs = '?' , type = str , help = "online running" , default = "false")
args = parser.parse_args()



def create_connection():
	CONNECTION = "postgres://postgres:postgres@localhost:5431/postgres"
	conn = psycopg2.connect(CONNECTION)
			


def run_query(query, rangeL = args.range, rangeUnit = args.rangeUnit, n_st = args.def_st, n_s = args.def_s, n_it = args.n_it):
	# Connect to the system
	CONNECTION = "postgres://postgres:postgres@localhost:5431/postgres"
	conn = psycopg2.connect(CONNECTION)
	cursor = conn.cursor()
	

	if rangeUnit in ["week","w","Week"]:
		rangeUnit = "day"
		rangleL = rangeL*7
		
	runtimes = []
	full_time = time.time()
	for it in tqdm(range(n_it)):
		date = random_date(args.min_ts, args.max_ts, set_date[(int(rangeL)*it)%500], dform = '%Y-%m-%dT%H:%M:%S')
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
		q_interpolate_avg = 'interpolate(avg(' + li[0] + '))'
		for j in li[1:]:
			q += ', ' + j
			# q_filter += ' OR ' + j + ' > 0.95'
			q_avg += ', ' + 'avg(' + j + ')'
			q_interpolate_avg += ', interpolate(avg(' + j + '))'
		temp = temp.replace("<sid>", q)
		temp = temp.replace("<sid1>", str(set_s[(rangeL*it)%500]))
		temp = temp.replace("<sid2>", str(set_s[(rangeL*(it+1))%500]))
		temp = temp.replace("<sid3>", str(set_s[(rangeL*(it+2))%500]))
		temp = temp.replace("<interpolate_avg>", q_interpolate_avg)
		temp = temp.replace("<sfilter>", q_filter + ')')
		temp = temp.replace("<avg_s>", q_avg)
		
		start = time.time()
		# print(temp)
		cursor.execute(temp)
		results_ = cursor.fetchall()

		diff = (time.time()-start)*1000
		#  print(temp, diff)
		runtimes.append(diff)
		if time.time() - full_time > args.timeout and it > 5: 
			break  
				
	conn.close()
	return stats.mean(runtimes), stats.stdev(runtimes)



db_name = "timescaledb"

from threading import Thread
from threading import Event
def input_data(event):
	from online_library import generate_continuing_data
	CONNECTION = "postgres://postgres:postgres@localhost:5431/postgres"
	conn = psycopg2.connect(CONNECTION)
	conn.autocommit = True
	cur = conn.cursor()
	data = generate_continuing_data()
	insertion_sql_head = "insert into d1 (time, id_station ," + ",".join(["s"+str(i) for i in range(100)]) + ")"
	values = [f"('{data['time_stamps'][i]}', '{data['stations'][i]}', {', '.join([str(s_n) for s_n in data['sensors'][i]])})" for i in range(10000)]
	sql = insertion_sql_head + " VALUES " + ",".join(values)
	while True:
		#data = generate_continuing_data()
		#insertion_sql_head = "insert into d1 (time, id_station ," + ",".join(["s"+str(i) for i in range(100)]) + ")"
		#values = [f"('{data['time_stamps'][i]}', '{data['stations'][i]}', {', '.join([str(s_n) for s_n in data['sensors'][i]])})" for i in range(10000)]
		#sql = insertion_sql_head + " VALUES " + ",".join(values)
		cur.execute(sql)
		#cur.execute("select count(*) from d1")
		#res_2 = cur.fetchall()		
		#print("input")
		if event.is_set():
			break	
		#print("amount_of_data" , res_2)

rate = 2000
if __name__ == "__main__":
	show_loading_bar = False

	if False:#args.online == "true":
		event = Event()
		with open('queries.sql') as file:
			queries = [line.rstrip() for line in file]
		query = queries[0].replace("<db>", "d1",)
		for i in range(10):
			thread = Thread(target=input_data, args=(event,))
			thread.start()
			import time 
			time.sleep(20)
			print(run_query(query))	

	
	print(f"running {db_name}")
	run_system(args,"timescaledb",run_query)
	event.set()

