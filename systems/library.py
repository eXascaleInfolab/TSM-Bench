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


def plot_query_directory(query_dir):
	import sys
	import matplotlib.pyplot as plt

	plot_dir = f"{query_dir}/plots"
	selected_query = query_dir.split("/")[-1]
	
	if not os.path.exists(plot_dir):
		os.mkdir(plot_dir)
	db_txt_files = sorted([ f_name for f_name in os.listdir(query_dir) if f_name.endswith(".txt")])

	results = { file_n.split(".")[0] :  pd.read_csv(query_dir+"/"+file_n,index_col=0) for file_n in db_txt_files}
	print("results to plot",results)
	## splits scenarios

	stations_scenario = { k : df[df.index.str.contains('st_')][["runtime"]] for k,df in results.items() }

	sensor_scenario = { k :df[df.index.str.contains('s_')][["runtime"]] for k,df in results.items() }

	time_scenario = { k : df[~df.index.str.contains('_')][["runtime"]] for k,df  in results.items() }

	combined_df = pd.concat([df.rename(columns={'runtime': key}) for key, df in stations_scenario.items()], axis=1)	
	combined_df.plot()
	plt.title(f"{selected_query} varying #stations")
	plt.savefig(f"{plot_dir}/stations.png")
	plt.close()

	combined_df = pd.concat([df.rename(columns={'runtime': key}) for key, df in sensor_scenario.items()], axis=1)
	combined_df.plot()
	plt.title(f"{selected_query} varying #sensors")
	plt.savefig(f"{plot_dir}/sensors.png")
	plt.close()



	combined_df = pd.concat([df.rename(columns={'runtime': key}) for key, df in time_scenario.items()], axis=1)

	combined_df.plot()
	plt.title(f"{selected_query} varying time range")
	plt.savefig(f"{plot_dir}/time_range.png")
	plt.close()

def run_system(args,system_name,run_query_f, query_filters = ("SELECT",)):
	with open("../scenarios.json") as file:
        	scenarios = json.load(file)

	n_stations , n_sensors , n_time_ranges = scenarios["stations"],  scenarios["sensors"], scenarios["time_ranges"]
	# Read Queries
	with open('queries.sql') as file:
		queries = [line.rstrip() for line in file]


	results_dir = "../../results"
	if not os.path.exists(results_dir):
		os.mkdir(results_dir)


	runtimes = []
	index_ = []
	for dataset in args.datasets:
		data_dir = f"{results_dir}/{dataset}"
		if not os.path.exists(data_dir):
			os.mkdir(data_dir)
		for i, query in enumerate(queries):
			try:
				query_dir = f"{data_dir}/q{i+1}"
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
					plot_query_directory(query_dir)
				else:
					print(f"query q{i+1} not run")
			except Exception as E:
				raise E
			runtimes = []
			index_ = []
			try:
				plot_query_directory(query_dir)
			except ValueError:
				pass # no objects to concatenate
			     
