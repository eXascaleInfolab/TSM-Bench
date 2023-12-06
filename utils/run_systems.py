import json
import os
from utils.plotting.plot_query_dir import plot_query_directory


result_dir = "results"

def run_system(args, system_name, run_query_f, query_filters=("SELECT",)):
    with open("systems/scenarios.json") as file:
        scenarios = json.load(file)

    default_n_iter = int(scenarios["n_runs"])
    default_timeout = scenarios["timeout"]  # Read Queries
    n_stations, n_sensors, n_time_ranges = scenarios["stations"], scenarios["sensors"], scenarios["time_ranges"]


    with open('queries.sql') as file:
        queries = [line.rstrip() for line in file]

    results_dir = "../../results"
    if not os.path.exists(results_dir):
        os.mkdir(results_dir)
    results_dir = "../../results/offline"
    if not os.path.exists(results_dir):
        os.mkdir(results_dir)

    log_file = "../../tsm_eval_error_log.txt"

    runtimes = []
    index_ = []
    try:
        for dataset in args.datasets:
            data_dir = f"{results_dir}/{dataset}"
            if not os.path.exists(data_dir):
                os.mkdir(data_dir)
            for i, query in enumerate(queries):
                try:
                    query_dir_ = f"{data_dir}/q{i + 1}"
                    if not os.path.exists(query_dir_):
                        os.mkdir(query_dir_)
                    query_dir = f"{data_dir}/q{i + 1}/runtime"
                    if not os.path.exists(query_dir):
                        os.mkdir(query_dir)
                    if all([f in query.upper() for f in query_filters]) and "q" + str(i + 1) in args.queries:
                        query = query.replace("<db>", dataset)
                        for range_unit in n_time_ranges:
                            try:
                                print("vary range", range_unit)
                                runtimes.append(run_query_f(query, rangeUnit=range_unit))
                                index_.append(f" {range_unit}")
                            except Exception as E:
                                import traceback
                                print(E)
                                runtimes.append((-1, -1))
                                index_.append(f" {range_unit}")
                                with open(log_file, 'a') as error_file:
                                    error_file.write(f"#############{system_name}#########")
                                    error_file.write(f"######Query{i + 1}#####")
                                    error_file.write(f"######Range Scenario{range_unit}#####")
                                    traceback.print_exc(file=error_file)
                                break
                        for sensors in n_sensors:
                            try:
                                print("vary sensors", sensors)
                                runtimes.append(run_query_f(query, n_s=sensors))
                                index_.append(f" s_{sensors}")
                            except Exception as E:
                                import traceback
                                print(E)
                                runtimes.append((-1, -1))
                                index_.append(f" s_{sensors}")
                                with open(log_file, 'a') as error_file:
                                    error_file.write(f"#############{system_name}#########")
                                    error_file.write(f"######Query{i + 1}#####")
                                    error_file.write(f"######Sensor Scenario{sensors}#####")
                                    traceback.print_exc(file=error_file)
                                break

                        for stations in n_stations:
                            try:
                                print("vary station", stations)
                                runtimes.append(run_query_f(query, n_st=stations))
                                index_.append(f"st_{stations}")
                            except Exception as E:
                                import traceback
                                print(E)
                                runtimes.append((-1, -1))
                                index_.append(f"st_{stations}")
                                with open(log_file, 'a') as error_file:
                                    error_file.write(f"#############{system_name}#########")
                                    error_file.write(f"######Query{i + 1}#####")
                                    error_file.write(f"######Station Scenario{stations}#####")
                                    traceback.print_exc(file=error_file)
                                break

                        runtimes = pd.DataFrame(runtimes, columns=['runtime', 'stddev'], index=index_)
                        print(runtimes)
                        runtimes.to_csv(f"{query_dir}/{system_name}.txt")
                        plot_query_directory(query_dir_)
                    else:
                        print(f"query q{i + 1} not run")
                except Exception as E:
                    raise E
                runtimes = []
                index_ = []
                try:
                    plot_query_directory(query_dir_)
                    print("plotting")
                except ValueError as E:
                    print("")
                    # print(E)
                    pass  # no objects to


    except Exception as E:
        import traceback
        from subprocess import Popen, PIPE, DEVNULL, STDOUT
        traceback.print_exc()
        print(E)