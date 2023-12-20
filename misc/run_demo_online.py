import pandas
import os

import sys

from systems.utils.online_library import generate_continuing_data

sys.path.append(os.getcwd())

from utils.system_modules import system_module_map
from utils.query_template_loader import load_query_tempaltes
import argparse

parser = argparse.ArgumentParser(description='Script for running any eval')

parser.add_argument('--system', nargs="?",
                    type=lambda x: str(x) if str(x) in system_module_map.keys()
                    else exit(f"system {x} not valid must be one of {list(system_module_map.keys())}"),
                    help='system name', required=True)

parser.add_argument('--it', nargs="?", type=int, help='n_iterationss', default=100)

args = parser.parse_args()

system = args.system
print(system)

dataset = "d1"

result_path = f"utils/online_queries/{dataset}"
os.makedirs(result_path, exist_ok=True)
output_file = f"{result_path}/{system}.csv"
log_file = f"{result_path}/{system}_log.csv"

with open(output_file, "w") as file:
    file.write("")

with open(log_file, "w") as file:
    file.write("")

n_iter = 10 #args.it
timeout = 1500
n_sensors = [10, 20, 40, 60, 80, 100]
n_stations = [1, 5, 10]
time_ranges = ["minute", "hour", "day", "week"]

scenarios = [(sensor, station, time_range) for sensor in n_sensors for station in n_stations for time_range in
             time_ranges]

from systems import timescaledb
system_module : timescaledb =  system_module_map[system]


batch_sizes = [10]#,20,50,100]

system_module.launch()

query_templates = load_query_tempaltes(system)
query_template = query_templates[0]
query = "q1"

for batch_size in batch_sizes:

    system_module.run_query()
    data = generate_continuing_data(args.batch_start + batch_size * 100, dataset)
    start_date = data["start_date"]
    print(start_date)
    #start insertion
    system_module.add_data(data, dataset)

    time, var = system_module.run_query(query, rangeUnit=time_range, rangeL=1, n_s=n_s, n_it=n_iter, n_st=n_st,
                                        dataset=dataset)


     query = query.replace("<db>", dataset)
        for n_s, n_st, time_range in scenarios:
            try:
                time, var = system_module.run_query(query, rangeUnit=time_range, rangeL=1, n_s=n_s, n_it=n_iter, n_st=n_st,
                                                    dataset=dataset)
                with open(output_file, "a") as file:
                    line = f"{time} , {var}  , q{i + 1} , {n_s} , {n_st} , {time_range}\n"
                    file.write(line)
            except Exception as E:
                with open(log_file, "a") as file:
                    line = f"{E}"
                    file.write(line)
                print(E)

finally:
    system_module.stop()
