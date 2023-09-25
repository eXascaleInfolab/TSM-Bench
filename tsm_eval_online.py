import argparse
import os
import sys
import subprocess
from systems.utils.time_settings import abr_time_map as unit_options
from systems import run_online 

from systems import  influx ,extremedb, timescaledb , questdb  , monetdb , clickhouse
system_module_map = { "influx" : influx,
	"extremedb" : extremedb,
    "clickhouse" : clickhouse,
	"questdb" : questdb,
    "monetdb" : monetdb,
	#"druid" : druid,
	"timescaledb" : timescaledb
	} 

datasets_choices = ['d1']

parser = argparse.ArgumentParser(description = 'Script for running any eval')
parser.add_argument('--system', nargs = '+', type = str, help = 'Systems name', default = ['clickhouse'])
parser.add_argument('--datasets', choices= datasets_choices, nargs = '*', type = str, help = 'Dataset name', default = ['d1'])
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
parser.add_argument('--batch_start', nargs = '?', type = int , help = 'Query execution timeout in seconds', default = 10)
parser.add_argument('--batch_step', nargs = '?', type = int , help = 'Query execution timeout in seconds', default = 100)
parser.add_argument('--n_threads', nargs = '?', type = int , help = 'Query execution timeout in seconds', default = 10)
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
    args.systems = ['clickhouse','influx','monetdb','questdb','timescaledb','extremedb']

if "all" in args.queries:
    args.queries = "q1,q2,q3,q4,q5,q6,q7"

if args.datasets == 'all':
    args.datasets = ['d1','d2']


queries = args.queries if "," not in args.queries  else args.queries.split(",") 

try: 
	systems = args.systems.split()
except: 
	systems = args.systems

system_paths = { system : os.path.join(os.getcwd(), "systems", system) for system in systems } 

from threading import Thread
from threading import Event
from systems.online_library import generate_continuing_data
import time
from subprocess import Popen, PIPE, STDOUT, DEVNULL

print("generating ingestion data")
data =  generate_continuing_data(args.batch_start+args.batch_step*100)

start_date  = data["time_stamps"][0]
start = data['time_stamps']

curr_wd = os.getcwd()

for dataset in args.datasets:
    for system in systems:
        systemPath = system_paths[system]
        if not(os.path.exists(systemPath)):
            sys.exit("Invalid system: " + system)

        system_module = system_module_map[system]

        print(f"###{system}###")


        os.chdir(systemPath)

        if args.host == "localhost":
            system_module.launch()

        elif system == "extremedb":
            system_module.launch(True) #only set the env variables

        print("starting insertion")
        batch_size = args.batch_start
        insertion_results = {} # run -> results 
        query_results = {}
        for i in range(0,20,3):
            event = Event()
            threads = []
            insertion_results[i] = [{"status" : "ok" , "insertions" : [] } for _ in range(args.n_threads)]
            try:
                for t_n in range(args.n_threads):
                    batch_size_ = batch_size
                    if system in ["questdb"]: #,"monetdb"
                        batch_size_ = batch_size*(args.n_threads)
                        if t_n > 0:
                            print("system can not handle multiple insertions")
                            break
                
                    try:
                        thread = Thread(target=system_module.input_data, args=(t_n,event,data,insertion_results[i][t_n] , batch_size_, args.host))
                        thread.start()
                        threads.append(thread)
                    except Exception as e:
                        if t_n > 0:
                            print(e)
                            print(f"{system} can only use a single thread for insertion, skipping additonal threads")
                            break
                        else:
                            raise e
            except Exception as e:
                print(e)
                print(f"{system} is not running or insertion rate not supported by system or aviable ressources")
                break	
            time.sleep(10)
            try:
                query_results[i] = run_online.run_system(args,system, system_module.run_system.run_query, (t_n+1)*batch_size)		
            except Exception as e:
                event.set()
                time.sleep(1)
                for thread in threads:
                    thread.join()
                raise e

            event.set()
            time.sleep(30)
            for thread in threads:
                print("joining threads")
                thread.join()

            batch_size = batch_size + args.batch_step


    ##store the result
        print(insertion_results)
        final_result  = {}   
        for batch_iteration, thread_results_full  in insertion_results.items():
            for query , (start , stop , mean , var) in query_results[batch_iteration].items():
                final_result[query] = final_result.get(query,{})   
                diff , insertion_rate  = stop-(start-1) , 0
                print(query)
                for t_n , thread_results in enumerate(thread_results_full):
                    print(type(thread_results),"BBBBBB")
                    insertions = thread_results["insertions"]
                    insertion_rate += sum([  rate  for time,rate in insertions if time >= start-1 and time <= stop ])/diff
                    if insertion_rate == 0:
                        print("insertions failed")
                    print(insertion_rate)
                final_result[query][batch_iteration] = (mean , var , insertion_rate)
                print("final_results" , final_result)
        run_online.save_online(final_result, system , dataset)
        #set the database to its initial state
        try:
            system_module.delete_data(host=args.host)
        except Exception as e :
            print("deletion failed")
            raise e

        if args.host == "localhost":
            process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
            stdout, stderr = process.communicate()

