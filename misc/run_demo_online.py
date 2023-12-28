import os

print(os.getcwd())
import sys

sys.path.append(os.getcwd())

from utils.ingestion.online_computer import DataIngestor

from utils.system_modules import system_module_map
from utils.query_template_loader import load_query_tempaltes
import argparse

parser = argparse.ArgumentParser(description='Script for running any eval')

parser.add_argument('--system', nargs="?",
                    type=lambda x: str(x) if str(x) in system_module_map.keys()
                    else exit(f"system {x} not valid must be one of {list(system_module_map.keys())}"),
                    help='system name', required=True)
parser.add_argument('--host', nargs="?",
                    type=str,
                    help='host address', required=True)

parser.add_argument('--query', nargs="?",
                    type=str,
                    help='host address', default="q1")

parser.add_argument('--it', nargs="?", type=int, help='n_iterationss', default=100)

args = parser.parse_args()

system = args.system
host = args.host
print(system)

dataset = "d1"

result_path = f"utils/online_queries/{dataset}"
os.makedirs(result_path, exist_ok=True)
output_file = f"{result_path}/{system}.csv"
log_file = f"{result_path}/{system}_log.csv"

n_iter = 100  # args.it
timeout = 1500
n_sensors = [10, 20, 40, 60, 80, 100]
n_stations = [1, 5, 10]
time_ranges = ["minute", "hour", "day", "week"]

query = args.query

from systems import timescaledb

n_rows = [10, 20, 60, 100, 140]  # *100 for the batch size
n_threads = 10

system_module: timescaledb = system_module_map[system]
system_module.launch()

query_templates = load_query_tempaltes(system)
query_template = query_templates[int(query[1:])-1]
query_template = query_template.replace("<db>", dataset)
query = "q1"


try:
    for n_rows in n_rows:
        scenarios = [(sensor, station, time_range) for sensor in n_sensors for station in n_stations for time_range in
                     time_ranges]

        while len(scenarios) > 0:
            ingestor = DataIngestor(system, system_module, dataset, n_rows_s=n_rows, max_runtime=2000, host=host,
                                    n_threads=n_threads)
            while True and len(scenarios) > 0:
                n_s, n_st, time_range = scenarios.pop(0)
                try:
                    with ingestor:
                        if not ingestor.check_ingestion_rate():
                            raise Exception(f"ingestion failed")
                        try:
                            time, var = system_module.run_query(query_template, rangeUnit=time_range, rangeL=1, n_s=n_s,
                                                                n_it=n_iter,
                                                                n_st=n_st,
                                                                dataset=dataset)
                            with open(output_file, "a") as file:
                                line = f"{time} , {var}  , query, {n_s} , {n_st} , {time_range} , {n_rows * n_threads * 100}\n"
                                file.write(line)
                        except Exception as E:
                            with open(log_file, "a") as file:
                                line = f"{E}\n"
                                file.write(line)
                            print(E)
                except Exception as E:
                    with open(log_file, "a") as file:
                        line = f"{E}\n"
                        file.write(line)
                    print(E)

finally:
    print("stopping system")
    system_module.stop()
