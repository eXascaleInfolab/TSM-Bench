import argparse
import os
import sys
import subprocess
from systems.utils.time_settings import abr_time_map as unit_options
from systems import launch_online

from systems import  influx ,extremedb, timescaledb , questdb , druid , monetdb , clickhouse

system_module_map = { "influx" : influx,
	"extremedb" : extremedb,
	"clickhouse" : clickhouse,
	"questdb" : questdb,
	"monetdb" : monetdb,
	"druid" : druid,
	"timescaledb" : timescaledb
	} 

parser = argparse.ArgumentParser(description = 'Script for running any eval')
parser.add_argument('--systems', nargs = '+', type = str, help = 'Systems name', default = ['clickhouse','druid','influx','monetdb','questdb','timescaledb'])
parser.add_argument('--datasets', nargs = '*', type = str, help = 'Dataset name', default = 'd1')
parser.add_argument('--queries', nargs = '*', type = str, help = 'List of queries to run (Q1-Q7)', default = "q1 q2 q3 q4 q5 q6 q7")
parser.add_argument('--n_st', nargs = '?', type = int, help = 'Number of stations in the dataset', default = 10)
parser.add_argument('--n_s', nargs = '?', type = int, help = 'Number of sensors in the dataset', default = 100)
parser.add_argument('--nb_st', nargs = '?', type = int, help = 'Default number of queried stations', default = 1)
parser.add_argument('--nb_sr', nargs = '?', type = int, help = 'Default number of queried sensors', default = 3)
parser.add_argument('--range', nargs = '?', type = str, help = 'Query range', default = "1d")
parser.add_argument('--max_ts', nargs = '?', type = str, help = 'Maximum query timestamp', default = "2019-04-30T00:00:00")
parser.add_argument('--min_ts', nargs = '?', type = str, help = 'Minimum query timestamp', default = "2019-04-01T00:00:00")
parser.add_argument('--timeout', nargs = '?', type = str, help = 'Query execution timeout in seconds', default = 20)
parser.add_argument('--additional_arguments', nargs = '?', type = str, help = 'Additional arguments to be passed to the scripts', default = '')
parser.add_argument('--online', nargs = '?', type = lambda x : str(x).lower() , help = 'Query execution timeout in seconds', default = "false")
parser.add_argument('--host', nargs = '?', type = str , help = 'Query execution timeout in seconds', default = "localhost")
parser.add_argument('--batchsize', nargs = '?', type = int , help = 'Query execution timeout in seconds', default = "500")
parser.add_argument('--n_threads', nargs = '?', type = int , help = 'Query execution timeout in seconds', default = 1)
args = parser.parse_args()


try:
    index = 0
    while index < len(args.range) and args.range[index].isdigit():
        index += 1
    args.rangeUnit = args.range[index:]
    args.range = int(args.range[:index])
    assert args.rangeUnit.upper() in ['S','M','H','D','W']
except:
    print("Input string does not conform to the expected format.", args.rangeUnit.upper())
    args.range = 1
    args.rangeUnit = "day"


if args.systems[0] == "all":
    args.systems = ['clickhouse','influx','monetdb','questdb','timescaledb','extremedb','druid']

if "all" in args.queries:
    args.queries = "q1,q2,q3,q4,q5,q6,q7"

if args.datasets == 'all':
    args.datasets = ['d1','d2']

datasets = ['d1', 'd2']

queries = args.queries if "," not in args.queries  else args.queries.split(",") 

try: 
	systems = args.systems.split()
except: 
	systems = args.systems

for d in args.datasets: 	
	if d not in datasets:
		sys.exit("Invalid dataset name: " + args.dataset)

system_paths = { system : os.path.join(os.getcwd(), "systems", system) for system in systems } 



from threading import Thread
from threading import Event
from systems.online_library import generate_continuing_data
import time
data =  generate_continuing_data() 
start_date  = data["time_stamps"][0]
start = data['time_stamps']


for system in systems:
	systemPath = system_paths[system]
	if not(os.path.exists(systemPath)):
		sys.exit("Invalid system: " + system)

	system_module = system_module_map[system]
	
	print(f"###{system}###")

	curr_wd = os.getcwd()
	
	os.chdir(systemPath)

	if args.host == "localhost":
		system_module.launch()
	
	event = Event()
	print("starting insertion")
	threads = []
	for i in range(args.n_threads):
		thread = Thread(target=system_module.input_data, args=(event,data, args.batchsize, args.host))
		thread.start()	
		threads.append(thread)

	time.sleep(10)		
	try:
		launch_online.run_system(args,system, system_module.run_system.run_query)		
	except Exception as e:
		event.set()
		time.sleep(1)
		for thread in threads:
			thread.join()
		raise e

	event.set()
	time.sleep(1)
	for thread in threads:
		thread.join()

	try:
		system_module.delete_data(host=args.host)
	except Exception as e :
		print("deletion failed")
		raise e

	if args.host == "localhost":
		from subprocess import Popen, PIPE, STDOUT, DEVNULL
		process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
		stdout, stderr = process.communicate()	
	

