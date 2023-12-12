import pandas
import os
print(os.getcwd())
import sys
sys.path.append(os.getcwd())

from utils.system_modules import system_module_map
from utils.query_template_loader import load_query_tempaltes

system="influx"
dataset = "d1"

result_path = f"utils/full_results/{dataset}"
os.makedirs( result_path , exist_ok = True)
output_file = f"{result_path}/{system}.csv"

with open(output_file, "w") as file:
    file.write("")

n_iter = 10
timeout = 500
n_sensors = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
n_stations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
time_ranges = ["minute", "hour", "day", "week", "month"]



scenarios = [(sensor, station, time_range) for sensor in n_sensors for station in n_stations for time_range in
             time_ranges]


system_module = system_module_map[system]

system_module.launch()
query_templates = load_query_tempaltes(system)
print(query_templates)
for i, query in enumerate(query_templates):
    if "select" not in query.lower():
        continue
    query = query.replace("<db>", dataset)
    for n_s, n_st, time_range in scenarios:
        try:
            time, var = system_module.run_query(query, rangeUnit=time_range, rangeL=1, n_s=n_s, n_it=n_iter, n_st=n_st,dataset=dataset)
        except Exception as E:
            print(E)
            time, var = "fail", str(E)
        with open(output_file, "a") as file:
            line = f"{time} , {var}  , q{i+1} , {n_s} , {n_st} , {time_range}/n"
            file.write(line)
system_module.launch()
