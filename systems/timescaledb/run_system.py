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


import psycopg2

# Generate Random Values
random.seed(1)
set_st = [str(random.randint(0,9)) for i in range(500)]
set_s = [str(random.randint(0,99)) for i in range(500)]
set_date = [random.random() for i in range(500)]

def run_query(query, rangeL , rangeUnit , n_st , n_s , n_it, host="localhost"):
	# Connect to the system
	CONNECTION = f"postgres://postgres:postgres@{host}:5431/postgres"
	conn = psycopg2.connect(CONNECTION)
	cursor = conn.cursor()
	

	if rangeUnit in ["week","w","Week"]:
		rangeUnit = "day"
		rangleL = rangeL*7
		
	runtimes = []
	full_time = time.time()
	for it in tqdm(range(n_it)):
		date = random_date("2019-04-30T00:00:00", "2019-04-01T00:00:00" , set_date[(int(rangeL)*it)%500], dform = '%Y-%m-%dT%H:%M:%S')
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
	
		# sensors
		li = ['s' + str(z) for z in random.sample(range(100), n_s)]
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
		if time.time() - full_time > 100 and it > 5: 
			break  
				
	conn.close()
	return stats.mean(runtimes), stats.stdev(runtimes)



db_name = "timescaledb"
if __name__ == "__main__":
	print('launching timescaledb')
	args =init_parser() 

	import os
	import subprocess
	from subprocess import Popen, PIPE, STDOUT, DEVNULL # py3k

	process = Popen(['sh', 'variables.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
	stdout, stderr = process.communicate()

	process = Popen(['sh', 'launch.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
	stdout, stderr = process.communicate()

	process = Popen(['sleep', '10'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
	stdout, stderr = process.communicate()
	show_loading_bar = False	
	print(f"running {db_name}")	

	def query_f(query, rangeL = args.range, rangeUnit = args.rangeUnit, n_st = args.def_st, n_s = args.def_s, n_it = args.n_it):
                return run_query(query, rangeL = rangeL, rangeUnit = rangeUnit, n_st = n_st, n_s = n_s, n_it = n_it)

	run_system(args,"timescaledb",query_f)

