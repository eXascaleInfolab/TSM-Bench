import os
import atexit
from threading import Thread
from threading import Event
from systems.online_library import generate_continuing_data
import json
import pandas as pd

color_dict = {'clickhouse': "blue",
  "druid" :  'orange', 
  "extremedb" : "darkblue" ,
  "influx" : "pink" ,
  "monetdb" : "cyan",
  "questdb" : "grey" ,
  "timescaledb" : "black"} 





def run_system(args, system_name, run_query_f, query_filters=("SELECT",)):
    with open("../scenarios.json") as file:
        scenarios = json.load(file)

    with open('queries.sql') as file:
        queries = [line.rstrip() for line in file]

    results_dir = "../../results"
    if not os.path.exists(results_dir):
        os.mkdir(results_dir)

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
                        batch_size = args.batchsize
                 
                        query = query.replace("<db>", dataset)
                        runtime_mean , runtime_var = run_query_f(query, n_s = 10 , n_it = 100, n_st = 1, rangeL = 1, rangeUnit = "day" ,host=args.host)

                        if os.path.exists(system_file):
                            with open(system_file, "a") as file:
                                file.write(f"{batch_size},{runtime_mean},{runtime_var}\n")
                        else:
                            with open(system_file, "w") as file:
                                file.write(f" rate/s , runtime , runtime_var \n")
                                file.write(f"{batch_size},{runtime_mean},{runtime_var}\n")
                
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
