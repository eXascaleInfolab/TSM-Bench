import os

import sys

sys.path.append(os.getcwd())

from utils.ingestion.data_ingestion import DataIngestor
from utils.system_modules import system_module_map
from utils.query_template_loader import load_query_templates
import argparse

# questdb requieres dataset path to be rebuild
HOST_DATASET_PATH = "home/luca/TSM/TSM-BENCH/datasets"
dataset = "d1"
n_threads = 100

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

parser.add_argument('--batch_size', "-bs", nargs="?",
                    type=int,
                    help='number of datapoints  to insert', default=10000)

parser.add_argument('-oc', action='store_false', help='omit cleaning database')

parser.add_argument('--it', nargs="?", type=int, help='n_iterationss', default=100)

args = parser.parse_args()

clean_database = args.oc

system = args.system
host = args.host
batch_size = args.batch_size
print(system)

HOST_DATASET_PATH = os.path.join(HOST_DATASET_PATH, dataset + ".csv")
os.environ["HOST_DATASET_PATH"] = HOST_DATASET_PATH

result_path = f"utils/online_queries/{dataset}"
os.makedirs(result_path, exist_ok=True)
output_file = f"{result_path}/{system}.csv"
log_file = f"{result_path}/{system}_log.csv"

n_iter = 200  # args.it
timeout = 1500
n_sensors = [3]  # , 20, 40, 60, 80, 100]
n_stations = [1]  # , 5, 10]
time_ranges = ["day"]  # , "hour", "day", "week"]

query = args.query

from systems import timescaledb

n_rows = [int(batch_size / 100 / n_threads)]  # *100 for the batch size * 10 for the threads

#  quest db does not support multi threading for insertion
if system == "questdb":
    print("questdb does not support multi threading for insertion")
    n_threads = 1
    n_rows = [i * n_threads for i in n_rows]

system_module: timescaledb = system_module_map[system]

# system_module.launch()
query_templates = load_query_templates(system)

try:
    for n_rows in n_rows:
        scenarios = [(sensor, station, time_range) for sensor in n_sensors for station in n_stations for time_range in
                     time_ranges]

        while len(scenarios) > 0:
            ingestor = DataIngestor(system, system_module, dataset, n_rows_s=n_rows, max_runtime=200, host=host,
                                    n_threads=n_threads, clean_database=clean_database)
            try:
                with ingestor:
                    first = True
                    while len(scenarios) > 0:
                        if first:
                            first = False
                            n_s, n_st, time_range = scenarios[0]
                        else:
                            n_s, n_st, time_range = scenarios.pop(0)
                        if not ingestor.check_ingestion_rate():
                            break
                            raise Exception(f"ingestion failed")

                        for query_i, query_template in enumerate(query_templates):
                            query_name = "q" + str(query_i + 1)
                            if query.lower() == "empty":
                                continue
                            query_template = query_template.replace("<db>", dataset)
                            try:
                                time, var = system_module.run_query(query_template, rangeUnit=time_range, rangeL=1,
                                                                    n_s=n_s,
                                                                    n_it=n_iter,
                                                                    n_st=n_st,
                                                                    dataset=dataset, host=host)
                                with open(output_file, "a") as file:
                                    line = f"{time} , {var}  , {query_name} , {n_s} , {n_st} , {time_range} , {n_rows * n_threads * 100}\n"
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
                raise E

finally:
    print("stopping system")
    system_module.stop()
