from datetime import datetime
from tqdm import tqdm
import argparse
import os
import time
import statistics as stats
import numpy as np
import random
import json
import pandas as pd

def str_time_prop(start, end, time_format, prop):
	"""Get a time at a proportion of a range of two formatted times.
	start and end should be strings specifying times formatted in the
	given format (strftime-style), giving an interval [start, end].
	prop specifies how a proportion of the interval to be taken after
	start.  The returned time will be in the specified format.
	"""

	stime = time.mktime(time.strptime(start, time_format))
	etime = time.mktime(time.strptime(end, time_format))

	ptime = stime + prop * (etime - stime)

	return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop, dform = '%Y-%m-%dT%H:%M:%S'):
	return str_time_prop(start, end, dform, prop)
	
def get_list(elm, n_elm, max_r = 10, prefix = '', suffix = '', apostrophe = True):
	res = ''
	elms = random.sample(range(max_r), n_elm)
	for i in range(n_elm): 
		item = prefix + elm + str(elms[i]) +  suffix 
		if apostrophe: 
			item = "'" + item + "'"
		res += item 
		if i < n_elm - 1: 
			res += ", "
	return 
	
def to_pm(v):
		return str(int(v[0][0])) + "$" + '\\' + "pm$" + str(int(v[1][0]))

color_dict = {'clickhouse': "blue",
		"druid" :  'orange', 
		"extremedb" : "darkblue" ,
		"influx" : "pink" ,
		"monetdb" : "cyan",
		"questdb" : "grey" ,
		"timescaledb" : "black"} 

def plot_query_directory(query_dir):
	import sys
	import matplotlib.pyplot as plt
	runtime_dir = f"{query_dir}/runtime"
	plot_dir = f"{query_dir}/plots"
	selected_query = query_dir.split("/")[-1]
	
	if not os.path.exists(plot_dir):
		os.mkdir(plot_dir)
	db_txt_files = sorted([ f_name for f_name in os.listdir(runtime_dir) if f_name.endswith(".txt")])

	results = { file_n.split(".")[0] :  pd.read_csv(runtime_dir+"/"+file_n,index_col=0) for file_n in db_txt_files}
	#print("results to plot",results)
	## splits scenarios

	stations_scenario = { k : df[df.index.str.contains('st_')][["runtime"]] for k,df in results.items() }

	sensor_scenario = { k :df[df.index.str.contains('s_')][["runtime"]] for k,df in results.items() }

	time_scenario = { k : df[~df.index.str.contains('_')][["runtime"]] for k,df  in results.items() }

	combined_df = pd.concat([df.rename(columns={'runtime': key}) for key, df in stations_scenario.items()], axis=1)	
	combined_df.plot(color=[color_dict.get(x, '#333333') for x in combined_df.columns])
	plt.xlabel("# Stations")
	plt.ylabel("Runtime (ms)")
	plt.title(f"{selected_query} varying #stations")
	plt.savefig(f"{plot_dir}/stations.png")
	plt.close()

	combined_df = pd.concat([df.rename(columns={'runtime': key}) for key, df in sensor_scenario.items()], axis=1)
	combined_df.plot(color=[color_dict.get(x, '#333333') for x in combined_df.columns])
	plt.ylabel("Runtime (ms)") or plt.xlabel("# Sesnors")
	plt.title(f"{selected_query} varying #sensors")
	plt.savefig(f"{plot_dir}/sensors.png")
	plt.close()



	combined_df = pd.concat([df.rename(columns={'runtime': key}) for key, df in time_scenario.items()], axis=1)

	combined_df.plot(color=[color_dict.get(x, '#333333') for x in combined_df.columns])
	plt.ylabel("Runtime (ms)") or plt.xlabel("Query Range")
	plt.title(f"{selected_query} varying time range")
	plt.savefig(f"{plot_dir}/time_range.png")
	plt.close()

def run_system(args,system_name,run_query_f, query_filters = ("SELECT",)):
	with open("../scenarios.json") as file:
		scenarios = json.load(file)

	default_n_iter = int(scenarios["n_runs"])
	default_timeout = scenarios["timeout"]# Read Queries
	n_stations , n_sensors , n_time_ranges = scenarios["stations"],  scenarios["sensors"], scenarios["time_ranges"]
	with open('queries.sql') as file:
		queries = [line.rstrip() for line in file]


	results_dir = "../../results"
	if not os.path.exists(results_dir):
		os.mkdir(results_dir)


	runtimes = []
	index_ = []
	try:
		for dataset in args.datasets:
			data_dir = f"{results_dir}/{dataset}"
			if not os.path.exists(data_dir):
				os.mkdir(data_dir)
			for i, query in enumerate(queries):
				try:
					query_dir_ = f"{data_dir}/q{i+1}"
					if not os.path.exists(query_dir_):
						os.mkdir(query_dir_)
					query_dir = f"{data_dir}/q{i+1}/runtime"
					if not os.path.exists(query_dir):
						os.mkdir(query_dir)
					if all([f in query.upper() for f in query_filters]) and "q" + str(i+1) in args.queries :
						query = query.replace("<db>", dataset)
						for range_unit in n_time_ranges:
							print("vary range",range_unit)
							runtimes.append(run_query_f(query,rangeUnit=range_unit))
							index_.append(f" {range_unit}")
						for sensors  in n_sensors:
							print("vary sensors" , sensors)
							runtimes.append(run_query_f(query,n_s=sensors))
							index_.append(f" s_{sensors}")
						for stations in n_stations:
							print("vary station",stations)
							runtimes.append(run_query_f(query,n_st=stations))
							index_.append(f"st_{stations}")
						runtimes = pd.DataFrame(runtimes, columns=['runtime','stddev'], index=index_)
						print(runtimes)
						runtimes.to_csv(f"{query_dir}/{system_name}.txt")
						plot_query_directory(query_dir_)
					else:
						print(f"query q{i+1} not run")
				except Exception as E:
					raise E
				runtimes = []
				index_ = []
				try:
					plot_query_directory(query_dir_)
				except ValueError as E:
					print(E)
					pass # no objects to 


	except Exception as E:
		from subprocess import Popen, PIPE, DEVNULL , STDOUT
		process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
		stdout, stderr = process.communicate()
		print(E)    
    
def init_parser():
	with open("../scenarios.json") as file:
		scenarios = json.load(file)
	#n_stations , n_sensors , n_time_ranges = scenarios["stations"],  scenarios["sensors"], scenarios["time_ranges"]
	
	default_n_iter = int(scenarios["n_runs"])
	default_timeout = scenarios["timeout"]
	# Parse Arguments
	parser = argparse.ArgumentParser(description = 'Script for running any eval')
	parser.add_argument('--system', nargs = '*', type = str, help = 'System name', default = '')
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
	parser.add_argument('--n_it', nargs = '?', type = int, help = 'Minimum number of iterations', default = default_n_iter  )
	parser.add_argument('--timeout', nargs = '?', type = float, help = 'Query execution timeout in seconds', default = default_timeout)
	parser.add_argument('--additional_arguments', nargs = '?', type = str, help = 'Additional arguments to be passed to the scripts', default = '')
	args = parser.parse_args()
	return args

				 
