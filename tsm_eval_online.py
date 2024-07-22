import os

import sys

from utils.ingestion.data_ingestion import DataIngestor
from utils.plotting.plot_query_dir import plot_query_directory
from utils.run_query import run_query
from utils.system_modules import system_module_map
from utils.query_template_loader import load_query_templates
import argparse

# questdb requieres dataset path to be rebuild
HOST_DATASET_PATH = "./datasets"
dataset = "d1"
n_threads = 10

parser = argparse.ArgumentParser(description='Script to run the online queries')

parser.add_argument('--system', nargs="?",
                    type=lambda x: str(x) if str(x) in system_module_map.keys()
                    else exit(f"system {x} not valid must be one of {list(system_module_map.keys())}"),
                    help='system name', required=True)
parser.add_argument('--host', nargs="?",
                    type=str,
                    help='host address', required=True)

parser.add_argument('--queries', nargs="+",
                    type=str,
                    help='queries to run', default=["q1"])

parser.add_argument('--batch_size', "-bs", nargs="+",
                    type=int,
                    help='number of datapoints  to insert', default=[10000,20000,50000])

parser.add_argument('-oc', action='store_false', help='omit cleaning database')

parser.add_argument('--it', nargs="?", type=int, help='n_iterationss', default=100)

args = parser.parse_args()

clean_database = args.oc

system = args.system
host = args.host
batch_sizes = args.batch_size
print("running online evaluation on:", system)

result_path = f"results/online/{dataset}"
os.makedirs(result_path, exist_ok=True)
log_file = f"{result_path}/{system}_log.csv"

n_iter = 10  # args.it
timeout = 1500
n_sensors = [3]  # , 20, 40, 60, 80, 100]
n_stations = [1]  # , 5, 10]
time_ranges = ["day"]  # , "hour", "day", "week"]

queries = args.queries

print(queries)
if queries == 'all': 
  queries = ['q1', 'q2', 'q3', 'q4', 'q5'] 

from systems import timescaledb

# threads 10
# *100 for the batch size * 10 for the threads

#  quest db does not support multi threading for insertion
if system == "questdb":
    print("questdb does not support multi threading for insertion setting number of threads to 1")
    if HOST_DATASET_PATH is None:
        raise Exception("questdb requires the host datasetpath tto be set to clear up the database")

    HOST_DATASET_PATH = os.path.join(HOST_DATASET_PATH, dataset + ".csv")
    os.environ["HOST_DATASET_PATH"] = HOST_DATASET_PATH
    n_threads = 1

if system == "monetdb":
    n_threads = 1

n_rows = [int(batch_size / 100 / n_threads) for batch_size in batch_sizes]

system_module: timescaledb = system_module_map[system]

if host == "localhost":
    system_module.launch()

query_templates = load_query_templates(system)

try:
    for n_rows in n_rows:
        scenarios = [(sensor, station, time_range) for sensor in n_sensors for station in n_stations for
                     time_range in
                     time_ranges]

        ingestor = DataIngestor(system, system_module, dataset, n_rows_s=n_rows, max_runtime=1500, host=host,
                                n_threads=n_threads, clean_database=clean_database, warmup_time=10)
        try:
            with ingestor:
                first = True
                for query in queries:
                    query_path_path = f"results/online/{dataset}/{query}"
                    os.makedirs(f"{query_path_path}/runtimes", exist_ok=True)
                    output_file = f"{query_path_path}/runtimes/{system}.txt"
                    print('y', query)
                    query_template = query_templates[int(query[1:]) - 1]
                    for n_s, n_st, time_range in scenarios:
                        if query.lower() == "empty":
                            print("skipping empty query")
                            continue
                        print("running query:", query, "with", n_s, "sensors", n_st, "stations", time_range,
                              "time range")

                        query_template = query_template.replace("<db>", dataset)
                        try:
                            time, var = run_query(system_module, query_template, rangeUnit=time_range, rangeL=1,
                                                  n_s=n_s,
                                                  n_it=n_iter,
                                                  n_st=n_st,
                                                  dataset=dataset, host=host)
                            with open(output_file, "a") as file:
                                line = f"{time} , {var}  , {query} , {n_s} , {n_st} , {time_range} , {n_rows * n_threads * 100}\n"
                                file.write(line)
                        except Exception as E:
                            with open(log_file, "a") as file:
                                line = f"{E}\n"
                                file.write(line)
                            print(E)
                #plot_query_directory(query_path_path)
        except Exception as E:
            with open(log_file, "a") as file:
                line = f"{E}\n"
                file.write(line)
                print(E)
            raise E
finally:
    pass
