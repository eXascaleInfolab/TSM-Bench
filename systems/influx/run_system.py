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
sys.path.append("systems")

from library import random_date

from utils import *
from library import *

from influxdb import InfluxDBClient

# Generate Random Values
random.seed(1)
set_st = [str(random.randint(0,9)) for i in range(500)]
set_s = [str(random.randint(0,99)) for i in range(500)]
set_date = [random.random() for i in range(500)]

def run_query(query, rangeL , rangeUnit , n_st , n_s , n_it , host = "localhost" ):
	# Connect to the system
	client = InfluxDBClient(host=host, port=8086, username='luca')
	
	runtimes = []
	n_queries = []
	full_time = time.time()
	for it in tqdm(range(n_it)):
		date = random_date("2019-04-30T00:00:00", "2019-04-01T00:00:00", set_date[(int(rangeL)*it)%500], dform = '%Y-%m-%dT%H:%M:%S')
		temp = query.replace("<timestamp>", date)
		temp = temp.replace("<range>", str(rangeL))
		temp = temp.replace("<rangesUnit>", str(rangeUnit[0]))
		#print(date,temp)	
		# stations
		li = ['st' + str(z) for z in random.sample(range(100), n_st)]
		#  print(li)
		q = '(id_station =' + "'" + li[0] + "'"
		for j in li[1:]:
			q += ' OR '  + 'id_station =' + "'" + j + "'"
		q += ")"
		temp = temp.replace("<stid>", q)
	
		# sensors
		li = ['s' + str(z) for z in random.sample(range(10), n_s)]
		q = ",".join(li)
		q_filter = "( " + li[0] + ' > 0.95' +")"
		q_avg =  ",".join([f"mean({e})" for e in li])  #'mean(' + li[0] + ')'
		q_avg_ = ",".join([f"mean_{e}" for e in li])
		q_avg_as = ",".join([ f"mean({e})  as mean_{e}" for e in li])
                
		temp = temp.replace("<sid>", q)
		temp = temp.replace("<sid1>", str(set_s[(rangeL*it)%500]))
		temp = temp.replace("<sid2>", str(set_s[(rangeL*(it+1))%500]))
		temp = temp.replace("<sid>", q)
		temp = temp.replace("<sfilter>", q_filter )
		temp = temp.replace("<avg_s>", q_avg)                
		temp = temp.replace("<avg_s_>", q_avg_)                
		temp = temp.replace("<avg_s_as>", q_avg_as)
		
		start = time.time()
		queries = client.query(temp)
		##print(queries)
		diff = (time.time()-start)*1000

		runtimes.append(diff)
		if time.time() - full_time > 200 and it > 5: 
			break  
			
	client.close()
	return round(stats.mean(runtimes),3) , round(stats.stdev(runtimes),3)

if __name__ == "__main__":
	args = init_parser()

	import subprocess
	from subprocess import Popen, PIPE, STDOUT, DEVNULL # py3k

	script_dir = os.path.dirname(os.path.abspath(__file__))

	# Get the absolute path of the 'systems' directory (one level above)
	systems_dir = os.path.join(script_dir, '..', 'systems')
	sys.path.append(systems_dir)
	
	print("launching system")
	process = Popen(['sh', 'launch.sh', '&'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
	stdout, stderr = process.communicate()

	process = Popen(['sleep', '2'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
	stdout, stderr = process.communicate()	
	
	def query_f(query, rangeL = args.range, rangeUnit = args.rangeUnit, n_st = args.def_st, n_s = args.def_s, n_it = args.n_it, host = "localhost"):
		return run_query(query, rangeL = rangeL, rangeUnit = rangeUnit, n_st = n_st, n_s = n_s, n_it = n_it, host= host)
		
	run_system(args,"influx",query_f)

	process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
	stdout, stderr = process.communicate()

