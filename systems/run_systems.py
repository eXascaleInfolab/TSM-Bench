
import statistics as stats
import numpy as np
import random
import json
import pandas as pd

color_dict = {'clickhouse': "blue",
                "druid" :  'orange',
                "extremedb" : "darkblue" ,
                "influx" : "pink" ,
                "monetdb" : "cyan",
                "questdb" : "grey" ,
                "timescaledb" : "black"}

def plot_query_directory(query_dir):
        import sys
        import matplotlib.pyplot as plt
        runtime_dir = f"{query_dir}/runtime"
        plot_dir = f"{query_dir}/plots"
        selected_query = query_dir.split("/")[-1]

        if not os.path.exists(plot_dir):
                os.mkdir(plot_dir)
        db_txt_files = sorted([ f_name for f_name in os.listdir(runtime_dir) if f_name.endswith(".txt")])

        results = { file_n.split(".")[0] :  pd.read_csv(runtime_dir+"/"+file_n,index_col=0) for file_n in db_txt_files}
        #print("results to plot",results)
        ## splits scenarios

        stations_scenario = { k : df[df.index.str.contains('st_')][["runtime"]] for k,df in results.items() }

        sensor_scenario = { k :df[df.index.str.contains('s_')][["runtime"]] for k,df in results.items() }

        time_scenario = { k : df[~df.index.str.contains('_')][["runtime"]] for k,df  in results.items() }

        combined_df = pd.concat([df.rename(columns={'runtime': key}) for key, df in stations_scenario.items()], axis=1)
        combined_df.plot(color=[color_dict.get(x, '#333333') for x in combined_df.columns])
        plt.xlabel("# Stations")
        plt.ylabel("Runtime (ms)")
        plt.title(f"{selected_query} varying #stations")
        plt.savefig(f"{plot_dir}/stations.png")
        plt.close()

        combined_df = pd.concat([df.rename(columns={'runtime': key}) for key, df in sensor_scenario.items()], axis=1)
        combined_df.plot(color=[color_dict.get(x, '#333333') for x in combined_df.columns])
        plt.ylabel("Runtime (ms)") or plt.xlabel("# Sesnors")
        plt.title(f"{selected_query} varying #sensors")
        plt.savefig(f"{plot_dir}/sensors.png")
        plt.close()



        combined_df = pd.concat([df.rename(columns={'runtime': key}) for key, df in time_scenario.items()], axis=1)

        combined_df.plot(color=[color_dict.get(x, '#333333') for x in combined_df.columns])
        plt.ylabel("Runtime (ms)") or plt.xlabel("Query Range")
        plt.title(f"{selected_query} varying time range")
        plt.savefig(f"{plot_dir}/time_range.png")
        plt.close()

def run_system(args,system_name,run_query_f, query_filters = ("SELECT",)):
        with open("../scenarios.json") as file:
                scenarios = json.load(file)

        default_n_iter = int(scenarios["n_runs"])
        default_timeout = scenarios["timeout"]# Read Queries
        n_stations , n_sensors , n_time_ranges = scenarios["stations"],  scenarios["sensors"], scenarios["time_ranges"]
        with open('queries.sql') as file:
                queries = [line.rstrip() for line in file]


        results_dir = "../../results"
        if not os.path.exists(results_dir):
                os.mkdir(results_dir)


        runtimes = []
        index_ = []
        try:
                for dataset in args.datasets:
                        data_dir = f"{results_dir}/{dataset}"
                        if not os.path.exists(data_dir):
                                os.mkdir(data_dir)
                        for i, query in enumerate(queries):
                                try:
                                        query_dir_ = f"{data_dir}/q{i+1}"
                                        if not os.path.exists(query_dir_):
                                                os.mkdir(query_dir_)
                                        query_dir = f"{data_dir}/q{i+1}/runtime"
                                        if not os.path.exists(query_dir):
                                                os.mkdir(query_dir)
                                        if all([f in query.upper() for f in query_filters]) and "q" + str(i+1) in args.queries :
                                                query = query.replace("<db>", dataset)
                                                for range_unit in n_time_ranges:
                                                        print("vary range",range_unit)
                                                        runtimes.append(run_query_f(query,rangeUnit=range_unit))
                                                        index_.append(f" {range_unit}")
                                                for sensors  in n_sensors:
                                                        print("vary sensors" , sensors)
                                                        runtimes.append(run_query_f(query,n_s=sensors))
                                                        index_.append(f" s_{sensors}")
                                                for stations in n_stations:
                                                        print("vary station",stations)
                                                        runtimes.append(run_query_f(query,n_st=stations))
                                                        index_.append(f"st_{stations}")
                                                runtimes = pd.DataFrame(runtimes, columns=['runtime','stddev'], index=index_)
                                                print(runtimes)
                                                runtimes.to_csv(f"{query_dir}/{system_name}.txt")
							plot_query_directory(query_dir_)
                                        else:
							print(f"query q{i+1} not run")
                                except Exception as E:
                                        raise E
                                runtimes = []
                                index_ = []
                                try:
                                        print("plotting")
                                        plot_query_directory(query_dir_)
                                except ValueError as E:
                                        print("plotting failed")
                                        print(E)
                                        pass # no objects to


        except Exception as E:
                from subprocess import Popen, PIPE, DEVNULL , STDOUT
                process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
                stdout, stderr = process.communicate()
		print(E)
