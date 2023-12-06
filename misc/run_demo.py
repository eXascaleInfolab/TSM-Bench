import os
import sys
root_dir = f"{os.getcwd().split('TSM-Bench')[0]}/TSM-Bench"
os.chdir(root_dir)
print(os.getcwd())
sys.path.append(root_dir)
import pandas

from systems import (clickhouse, questdb , extremedb, druid, timescaledb, influx , monetdb)

def load_query_file(system):
    path = os.path.dirname(system.__file__)
    with open(f'{path}/queries.sql') as file: 
        queries = [line.rstrip() for line in file]
    return queries

# settings
n_sensors = [1,10,20,30,40,50,60,70,80,90,100]
n_stations =  [1,2,3,4,5,6,7,8,9,10] 
time_ranges = ["minute","hour","day","week","month"]
dataset = "d1"

n_iter = 2000
timeout = 5000

scenarios  = [(sensor, station, time_range) for sensor in n_sensors for station in n_stations for time_range in time_ranges]

systems = ( influx ,questdb, clickhouse , extremedb, timescaledb, monetdb)
output_file = "results/parameters.txt"

for system in systems:
    system.launch()
    system_name = system.__file__.split("/")[-2]
    queries = load_query_file(system)
    print(queries)
    for i ,query in enumerate(queries):
        query = query.replace("<db>", dataset)
        for n_s, n_st, time_range in scenarios:
            try:
                time , var = system.run_query(query , rangeUnit=time_range , rangeL = 1 , n_s=n_s , n_it=n_iter , n_st = n_st) 
            except Exception as E:
                print(E)
                time , var = "fail" , str(E)
            with open(output_file, "a") as file:
                line = f"{time} , {var}  , {i} , {n_s} , {n_st} , {time_range} , {system_name} \n"
                file.write(line)
    system.stop()