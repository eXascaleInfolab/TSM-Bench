import datetime

import pandas
import os

import sys

from utils.run_query import run_query

sys.path.append(os.getcwd())

from utils.system_modules import system_module_map
from utils.query_template_loader import load_query_templates
import argparse

parser = argparse.ArgumentParser(description='Script for running any eval')

parser.add_argument('--system', nargs="?",
                    type=lambda x: str(x) if str(x) in system_module_map.keys()
                    else exit(f"system {x} not valid must be one of {list(system_module_map.keys())}"),
                    help='system name', required=True)

parser.add_argument('--it', nargs="?", type=int, help='n_iterationss', default=10)

args = parser.parse_args()

system = args.system
print(system)

dataset = "d2"
result_path = f"utils/full_results/{dataset}"
os.makedirs(result_path, exist_ok=True)
output_file = f"{result_path}/{system}.csv"
log_file = f"{result_path}/{system}_log.csv"

if os.path.exists(output_file):
    pass
else:
    with open(output_file, "w") as file:
        file.write(f"runtime, var  , query , n_s , n_st , timerange \n")

with open(log_file, "w") as file:
    file.write("")

n_iter = args.it

n_sensors = [1, 20, 40, 60, 80, 100]
n_stations = [1, 10 , 50 , 100 , 400, 800, 1200, 1600, 2000]
time_ranges = ["minute", "hour", "day", "week"]

# scenarios = [(sensor, station, time_range) for sensor in n_sensors for station in n_stations for time_range in
#              time_ranges]

# stations last
scenarios = [(sensor, time_range, station) for sensor in n_sensors for time_range in time_ranges for station in
             n_stations]

from systems import timescaledb

system_module: timescaledb = system_module_map[system]

query_templates = load_query_templates(system)

already_computed_results = set()
with open(output_file, "r") as file:
    for line in file.readlines()[1:]:
        if line == "":
            continue
        r_, v_, q, n_s, n_st, time_range = line.split(",")
        already_computed_results.add((q.strip(), int(n_s), int(n_st), time_range.strip()))

print(already_computed_results)

try:
    system_module.launch()
    for i, query in enumerate(query_templates):
        if "select" not in query.lower():
            continue
        query = query.replace("<db>", dataset)
        for n_s, time_range, n_st in scenarios:
            if (f"q{i + 1}", n_s, n_st, time_range) in already_computed_results:
                print("already computed")
                continue
            print(f"running query {i + 1} with {n_s} sensors and {n_st} stations and {time_range}")
            try:
                time, var = run_query(system_module, query, rangeUnit=time_range, rangeL=1, n_s=n_s, n_it=n_iter,
                                                    n_st=n_st,
                                                    dataset=dataset)
                with open(output_file, "a") as file:
                    line = f"{time} , {var} , q{i + 1} , {n_s} , {n_st} , {time_range}\n"
                    file.write(line)
            except Exception as E:
                with open(log_file, "a") as file:
                    line = f"{E}"
                    file.write(line)
                print(E)

finally:
    system_module.stop()
