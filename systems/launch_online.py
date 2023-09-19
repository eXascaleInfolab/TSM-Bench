import os
import atexit
from threading import Thread
from threading import Event
from systems.online_library import generate_continuing_data
import json
import pandas as pd
import time 

color_dict = {'clickhouse': "blue",
  "druid" :  'orange', 
  "extremedb" : "darkblue" ,
  "influx" : "pink" ,
  "monetdb" : "cyan",
  "questdb" : "grey" ,
  "timescaledb" : "black"} 

def run_system(args, system_name, run_query_f, insertion_speed , query_filters=("SELECT",) ):
    with open("../scenarios.json") as file:
        scenarios = json.load(file)

    with open('queries.sql') as file:
        queries = [line.rstrip() for line in file]

    results_dir = "../../results"
    if not os.path.exists(results_dir):
        os.mkdir(results_dir)
    
    
    results = {} # query -> time_start , time_stop , mean_runtime , var_runtime
    try:
        for dataset in args.datasets:
            data_dir = f"{results_dir}/{dataset}"
            if not os.path.exists(data_dir):
                os.mkdir(data_dir)
            for i, query in enumerate(queries):
                try:
                    if all([f in query.upper() for f in query_filters]) and "q" + str(i+1) in args.queries:
                        query_dir = f"{data_dir}/q{i+1}_online"
                        if not os.path.exists(query_dir):
                            os.mkdir(query_dir)

                        system_file = f"{query_dir}/{system_name}.txt"
                        
                 
                        query = query.replace("<db>", dataset)
                        time_start = time.time()
                        runtime_mean , runtime_var = run_query_f(query, n_s = 10 , n_it = 100, n_st = 1, rangeL = 1, rangeUnit = "day" ,host=args.host)
                        time_stop = time.time()
                        results["q" + str(i+1)] = (time_start,time_stop,runtime_mean,runtime_var)
                     
                
                except Exception as E:
                    print("exception in query")
                    print(E)
                    raise E
                runtimes = []
                index_ = []

                try:
                    pass
                 
                    #print("plotting")
                    #plot_query_directory(query_dir_)
                except ValueError as E:
                    print("plotting failed")
                    print(E)
                    pass  # no objects to

    except Exception as E:
        print(E)
        
    return results

def save_online(results, system , dataset = "d1"):
    result_folder = "results"
    online_folder = f"{results_folder}/online"
    data_set_folder =  f"{online_folder}/{dataset}"
    
    os.makedirs(online_folder, exist_ok=True)
    os.makedirs(result_folder, exist_ok=True)
    os.makedirs(data_set_folder, exist_ok=True)
    
    for query,values in results:
        query_folder = f"{data_set_folder}/{query}"
        runtime_folder =  f"{query_folder}/runtime"
        plot_folder = f"{query_folder}/plots"
        
        os.makedirs(query_folder, exist_ok=True)
        os.makedirs(runtime_folder, exist_ok=True)
        os.makedirs(runtime_folder, exist_ok=True)
    
        
    
    
    
    
    
    
