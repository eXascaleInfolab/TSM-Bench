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


import os

import psycopg2

# Generate Random Values
random.seed(1)
set_st = [str(random.randint(0,9)) for i in range(500)]
set_s = [str(random.randint(0,99)) for i in range(500)]
set_date = [random.random() for i in range(500)]


def run_query(query, rangeL , rangeUnit, n_st , n_s , n_it , host="localhost"):
	# Connect to the system
	conn = psycopg2.connect(user="admin",
	  password="quest",
	  host=host,
	  port="8812",
	  database="d1")
	cursor = conn.cursor()
	options = {
		"day" : 60 * 60* 24,
	   "week" : 60 * 60* 24 * 7,
	   "minute" : 60,
	   "hour" : 60 * 60,
	   "second" : 1,
	   "month" : 60 * 60 * 24 * 30,
	   "year" :  60 * 60 * 24 * 30 * 12
	}
	
	runtimes = []
	n_queries = []
	full_time = time.time()
	for it in tqdm(range(n_it)):
		date = random_date("2019-04-01T00:00:00", "2019-04-30T00:00:00", set_date[(int(rangeL)*it)%500], dform = '%Y-%m-%dT%H:%M:%S')
		temp = query.replace("<timestamp>", date)
		temp = temp.replace("<range>", str(rangeL))
		temp = temp.replace("<rangesUnit>", str(options[rangeUnit.lower()]))
		
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
		temp = temp.replace("<sfilter>", q_filter + ')')
		temp = temp.replace("<avg_s>", q_avg)
		temp = temp.replace("<interpolate_avg>", q_interpolate_avg)

		start = time.time()
		
		cursor.execute(temp)
		queries = cursor.fetchall()
		n_queries.append(len(queries))
		diff = (time.time()-start)*1000
		runtimes.append(diff)
		if time.time() - full_time > 200 and it > 5: 
			break  
			
	conn.close()
	return stats.mean(runtimes), stats.stdev(runtimes) 

if __name__ == "__main__":
    print('launching system')

    import os
    import subprocess
    from subprocess import Popen, PIPE, STDOUT, DEVNULL # py3k
    
    args = init_parser() 

    process = Popen(['sh', 'variables.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    stdout, stderr = process.communicate()

    process = Popen(['sh', 'launch.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    stdout, stderr = process.communicate()

    process = Popen(['sleep', '3'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    stdout, stderr = process.communicate()
    
    def query_f(query, rangeL = args.range, rangeUnit = args.rangeUnit, n_st = args.def_st, n_s = args.def_s, n_it = args.n_it , host="localhost"):
        return run_query(query, rangeL=rangeL, rangeUnit = rangeUnit ,n_st = n_st , n_s = n_s , n_it = n_it,host=host)

    run_system(args,"questdb",query_f)	


    process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    stdout, stderr = process.communicate()

