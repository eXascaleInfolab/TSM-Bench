import argparse
import os
from systems.utils import run_online

from systems import influx, extremedb, timescaledb, questdb, monetdb, clickhouse
from utils.query_template_loader import load_query_templates

system_module_map = {"influx": influx,
                     "extremedb": extremedb,
                     "clickhouse": clickhouse,
                     "questdb": questdb,
                     "monetdb": monetdb,
                     "timescaledb": timescaledb
                     }

datasets_choices = ['d1']

parser = argparse.ArgumentParser(description='Script for running any eval')
parser.add_argument('--system', nargs='+', type=str, help='Systems name', default=['clickhouse'])
parser.add_argument('--datasets', nargs='*', type=str, help='Dataset name', default=['d1'])
parser.add_argument('--queries', nargs='*', type=str, help='List of queries to run (Q1-Q7)',
                    default="q1 q2 q3 q4 q5 q6 q7")
parser.add_argument('--n_st', nargs='?', type=int, help='Number of stations in the dataset', default=10)
parser.add_argument('--n_s', nargs='?', type=int, help='Number of sensors in the dataset', default=100)
parser.add_argument('--nb_st', nargs='?', type=int, help='Default number of queried stations', default=1)
parser.add_argument('--nb_sr', nargs='?', type=int, help='Default number of queried sensors', default=3)
parser.add_argument('--range', nargs='?', type=str, help='Query range', default="1d")
parser.add_argument('--max_ts', nargs='?', type=str, help='Maximum query timestamp', default="2019-04-30T00:00:00")
parser.add_argument('--min_ts', nargs='?', type=str, help='Minimum query timestamp', default="2019-04-01T00:00:00")
parser.add_argument('--timeout', nargs='?', type=str, help='Query execution timeout in seconds', default=20)
parser.add_argument('--additional_arguments', nargs='?', type=str,
                    help='Additional arguments to be passed to the scripts', default='')

parser.add_argument('--host', nargs='?', type=str, help='Query execution timeout in seconds', default="localhost")
parser.add_argument('--batch_start', nargs='?', type=int, help='Query execution timeout in seconds', default=10)
parser.add_argument('--batch_step', nargs='?', type=int, help='Query execution timeout in seconds', default=100)
parser.add_argument('--n_threads', nargs='?', type=int, help='Query execution timeout in seconds', default=10)
args = parser.parse_args()

try:
    index = 0
    while index < len(args.range) and args.range[index].isdigit():
        index += 1
    args.rangeUnit = args.range[index:]
    args.range = int(args.range[:index])
    assert args.rangeUnit.upper() in ['M', 'H', 'D', 'W']
except:
    print("Input string does not conform to the expected format.", args.rangeUnit.upper())
    args.range = 1
    args.rangeUnit = "day"

if args.system[0] == "all":
    args.system = ['clickhouse', 'influx', 'monetdb', 'questdb', 'timescaledb', 'extremedb']

if "all" in args.queries:
    args.queries = "q1,q2,q3,q4,q5,q6,q7"

if args.datasets == 'all':
    args.datasets = ['d1', 'd2']

args.queries = args.queries if "," not in args.queries else args.queries.split(",")

try:
    systems = args.system.split(",")
except:
    systems = args.system

system_paths = {system: os.path.join(os.getcwd(), "systems", system) for system in systems}

from threading import Thread
from threading import Event
from systems.utils.online_library import generate_continuing_data
import time
from subprocess import Popen, PIPE, STDOUT, DEVNULL

curr_wd = os.getcwd()

for dataset in args.datasets:
    data = generate_continuing_data(args.batch_start + args.batch_step * 100, dataset)
    start_date = data["start_date"]

    for system in systems:
        print(f"###{system}###")

        system_module = system_module_map[system]
        query_templates = load_query_templates(system)

        if args.host == "localhost":
            system_module.launch()

        elif system == "extremedb":
            system_module.launch(True)  # only set the env variables

        print("starting insertion")
        batch_size = args.batch_start
        insertion_results = {}  # run -> results
        query_results = {}
        for batch_iteration in [1,10]:
            event = Event()
            threads = []
            insertion_results[batch_iteration] = [{"status": "ok", "insertions": []} for _ in range(args.n_threads)]
            try:
                for t_n in range(args.n_threads):
                    batch_size_ = batch_size
                    if system in ["questdb"]:  # ,"monetdb"
                        batch_size_ = batch_size * (args.n_threads)
                        if t_n > 0:
                            print("system can not handle multiple insertions")
                            break

                    try:
                        thread = Thread(target=system_module.input_data, args=(
                            t_n, event, data, insertion_results[batch_iteration][t_n], batch_size_, args.host, dataset))
                        thread.start()
                        threads.append(thread)
                    except Exception as e:
                        if t_n > 0:
                            print(e)
                            print(f"{system} can only use a single thread for insertion, skipping additonal threads")
                            break
                        else:
                            raise e
            except Exception as e:
                print(e)
                print(f"{system} is not running or insertion rate not supported by system or aviable ressources")
                break
            time.sleep(10)

            ### run system queries
            try:
                query_runtimes = {}
                print("evaluating queries")
                for i, query in enumerate(query_templates):
                    if all([f in query.upper() for f in ("SELECT",)]) and "q" + str(i + 1) in args.queries:
                        print(f"{i+1}")
                        query = query.replace("<db>", dataset)
                        time_start = time.time()
                        runtime_mean, runtime_var = system_module.run_query(query, n_s=10, n_it=100, n_st=1,
                                                                            rangeL=1,
                                                                            rangeUnit="day", dataset=dataset,host=args.host)
                        time_stop = time.time()
                        query_runtimes["q" + str(i + 1)] = (time_start, time_stop, runtime_mean, runtime_var)
                query_results[batch_iteration] = query_runtimes
            except Exception as e:
                raise e

            finally:
                event.set()
                time.sleep(10)
                for thread in threads:
                    thread.join()
                try:
                    system_module.delete_data(date=start_date, host=args.host, dataset=dataset)
                except Exception as e:
                    print(e)
                    print("problem in data deletion")



            batch_size = batch_size + args.batch_step


        final_result = {}
        for batch_iteration, thread_results_full in insertion_results.items():
            for query, (start, stop, mean, var) in query_results[batch_iteration].items():
                final_result[query] = final_result.get(query, {})
                diff, insertion_rate = stop - (start - 1), 0
                # print(query)
                for t_n, thread_results in enumerate(thread_results_full):
                    insertions = thread_results["insertions"]
                    insertion_rate += sum(
                        [rate for time, rate in insertions if time >= start - 1 and time <= stop]) / diff
                    if insertion_rate == 0:
                        print("insertions failed")
                    print(insertion_rate)
                final_result[query][batch_iteration] = (mean, var, insertion_rate)
        print("storing results")
        run_online.save_online(final_result, system, dataset)


        if args.host == "localhost":
            system_module.stop()
