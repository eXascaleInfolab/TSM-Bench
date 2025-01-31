import argparse
import os
import json

import pandas as pd

from systems.config import system_names
from utils.plotting.plot_query_dir import plot_query_directory
from utils.query_template_loader import load_query_templates
from utils.run_query import run_query
from utils.tsm_eval_parser import init_main_parser
from utils.system_modules import system_module_map

datasets = ['d1', 'd2']


scenario = {
    "n_stations": [1,5,10],
    "n_sensors": [1,5,10,25,50,75,100],
    "n_time_ranges": ["hour", "day", "month"],
    "n_runs": 20,
    "timeout": 100,
}


args = init_main_parser(system_names, datasets  , scenario["n_runs"])

systems = args.systems
datasets = args.datasets

with open("systems/scenarios.json") as file:
    scenarios = json.load(file)

for dataset in datasets:

    for system in systems:
        system_module = system_module_map[system]
        try:
            system_module.launch()

            queries = load_query_templates(system)

            for i, query in enumerate(queries):
                if "q" + str(i + 1) in args.queries and "select" in query.lower():
                    runtimes = []
                    index_ = []

                    query = query.replace("<db>", dataset)

                    def default_query_f(rangeUnit=args.rangeUnit, n_st=args.n_st, n_s=args.n_s):
                        return run_query(system_module , query, rangeUnit=rangeUnit, n_st=n_st, n_s=n_s,
                                                       n_it=args.n_it, dataset=dataset, rangeL=1, host="localhost")


                    print("vary station:")
                    for stations in scenario["n_stations"]:
                        print(stations)
                        index_.append(f"st_{stations}")
                        try:
                            runtimes.append(default_query_f(n_st=stations))
                        except Exception as E:
                            import traceback

                            print(E)
                            runtimes.append((-1, -1))
                            break

                    runtimes = pd.DataFrame(runtimes, columns=['runtime', 'stddev'], index=index_)
                    print(runtimes)
                    query_dir = f"results/offline/{dataset}/q{i + 1}"
                    os.makedirs(query_dir + "/runtime", exist_ok=True)
                    runtimes.to_csv(f"{query_dir}/runtime/{system}.txt")
                    plot_query_directory(query_dir)
                else:
                    print(f"query q{i + 1} not run")

        # stop the system

        finally:
            system_module.stop()

