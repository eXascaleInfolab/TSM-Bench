import os
import atexit
from threading import Thread
from threading import Event
from systems.utils.online_library import generate_continuing_data
import json
import pandas as pd
import time 
import matplotlib.pyplot as plt


color_dict = {'clickhouse': "#7EC4C1",
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
 
    results = {} # query -> time_start , time_stop , mean_runtime , var_runtime
    try:
            for i, query in enumerate(queries):
                try:
                    if all([f in query.upper() for f in query_filters]) and "q" + str(i+1) in args.queries:
                                                
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
                
    except Exception as E:
        print(E)
    
    return results



def save_online(results, system , dataset = "d1"):
    """
    results example: {"q1": {0: (32.810654640197754, 4.215663565810583, 3013.800683366061), 1: (32.9471755027771, 3.527529676919926, 9040.327629569714), 2: (32.768380641937256, 4.02631751304756, 11352.204932450706), 3: (34.22324895858765, 6.082917765950305, 16224.66756258382), 4: (34.850499629974365, 7.843812471724312, 23042.998827768995), 5: (36.02532148361206, 21.486842912209163, 29851.482589288345), 6: (39.80292558670044, 43.30123477401164, 32427.02708199735), 7: (41.393070220947266, 62.19684029533341, 37617.33542302434), 8: (42.407965660095215, 37.60220738639919, 39740.24300552638), 9: (47.08098888397217, 67.07287381362472, 44031.71715851542)}}
    
    stores:
    .txt file -> system.txt
    insertion_rate , runtime , var
    3013.8006 , 32.8106 , 4.2156
                ....
    
    .png file putting all .txt files into one plot
    
    """
    result_folder = "results"
    online_folder = f"{result_folder}/online"
    data_set_folder =  f"{online_folder}/{dataset}"
    
    os.makedirs(online_folder, exist_ok=True)
    os.makedirs(result_folder, exist_ok=True)
    os.makedirs(data_set_folder, exist_ok=True)
    

    for query, values in results.items():
        query_folder = f"{data_set_folder}/{query}"
        runtime_folder =  f"{query_folder}/runtime"
        plot_folder = f"{query_folder}/plots"

        os.makedirs(query_folder, exist_ok=True)
        os.makedirs(plot_folder, exist_ok=True)
        os.makedirs(runtime_folder, exist_ok=True)
        txt_file_path = f"{runtime_folder}/{system}.txt"
        with open(txt_file_path, 'w') as txt_file:
            # Write the header line
            txt_file.write("insertion_rate , runtime , var\n")
            
            for index , (run_time , var , insertion_rate)  in values.items():
                txt_file.write(f"{insertion_rate:.4f} , {run_time:.4f} , {var:.4f}\n")
                
         #plot insertion_rate on x axis and runtime on y axis , labels are system names (e.g filename without .txt)
        txt_files = [ f"{runtime_folder}/{file_name}" for file_name in os.listdir(runtime_folder) if file_name.endswith(".txt") ]
        
        plt.figure(figsize=(10, 6))
        for txt_file_path in txt_files:
            system_name = os.path.splitext(os.path.basename(txt_file_path))[0]  # Extract system name from the file name
            insertion_rates , runtimes , variances = [] , [] , []
            
            with open(txt_file_path, 'r') as txt_file:
                lines = txt_file.readlines()[1:]  # Skip the header line
                for line in lines:
                    insertion_rate, runtime, var = map(float, line.strip().split(','))
                    insertion_rates.append(insertion_rate)
                    runtimes.append(runtime)
                    variances.append(var)
            # Create a scatter plot
        
            plt.plot(insertion_rates, runtimes, color = color_dict[system_name] , label = system_name)
            
        plt.xlabel('Insertion Rate per Second')
        plt.ylabel('Runtime')
        plt.title(f'{query} online')
        plt.legend()

        # Save the plot
        plot_file_path = f"{plot_folder}/{query}_online_plot.png"
        plt.savefig(plot_file_path)
        plt.close()
    
    
    
    
    
    
