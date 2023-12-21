import pandas
import os
print(os.getcwd())
import sys
sys.path.append(os.getcwd())

from utils.online_computer import DataIngestor


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

n_iter = 10  # args.it
timeout = 1500
n_sensors = [10]#, 20, 40, 60, 80, 100]
n_stations = [1]#, 5, 10]
time_ranges = ["minute"]#, "hour", "day", "week"]

scenarios = [(sensor, station, time_range) for sensor in n_sensors for station in n_stations for time_range in
             time_ranges]

from systems import timescaledb

batch_sizes = [10,100,1000]
host = "localhost"
n_threads = 2

system_module: timescaledb = system_module_map[system]
system_module.launch()

query_templates = load_query_tempaltes(system)
query_template = query_templates[0]
query_template = query_template.replace("<db>", dataset)
query = "q1"


try:
    for batch_size in batch_sizes:

        ingestor = DataIngestor(system_module, dataset, batch_size=batch_size, host=host,
                                n_threads=n_threads)
        with ingestor:
            for n_s, n_st, time_range in scenarios:
                try:
                    time, var = system_module.run_query(query_template, rangeUnit=time_range, rangeL=1, n_s=n_s, n_it=n_iter,
                                                        n_st=n_st,
                                                        dataset=dataset)
                    with open(output_file, "a") as file:
                        line = f"{time} , {var}  , query, {n_s} , {n_st} , {time_range}\n"
                        file.write(line)
                except Exception as E:
                    with open(log_file, "a") as file:
                        line = f"{E}"
                        file.write(line)
                    print(E)
        print(ingestor.insertion_stats)


finally:
    print("stopping system")
    system_module.stop()
