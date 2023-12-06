import argparse
import json 

def parse_args():
    with open("../scenarios.json") as file:
        scenarios = json.load(file)
    
    default_n_iter = int(scenarios["n_runs"])
    default_timeout = scenarios["timeout"]
    
    # Parse Arguments
    parser = argparse.ArgumentParser(description = 'Script for running any eval')
    parser.add_argument('--system', nargs = '*', type = str, help = 'System name', default = '')
    parser.add_argument('--dataset', nargs =  1 , type = str, help = 'Dataset name', default = 'd1')
    parser.add_argument('--queries', nargs = '?', type = str, help = 'List of queries to run (Q1-Q7)', default = ['q' + str(i) for i in range(1,8)])
    parser.add_argument('--nb_st', nargs = '?', type = int, help = 'Number of stations in the dataset', default = 10)
    parser.add_argument('--nb_s', nargs = '?', type = int, help = 'Number of sensors in the dataset', default = 100)
    parser.add_argument('--def_st', nargs = '?', type = int, help = 'Default number of queried stations', default = 1)
    parser.add_argument('--def_s', nargs = '?', type = int, help = 'Default number of queried sensors', default = 3)
    parser.add_argument('--range', nargs = '?', type = int, help = 'Query range', default = 1)
    parser.add_argument('--rangeUnit', nargs = '?', type = str, help = 'Query range unit', default = 'day')
    parser.add_argument('--max_ts', nargs = '?', type = str, help = 'Maximum query timestamp', default = "infer")#2019-04-30T00:00:00
    parser.add_argument('--min_ts', nargs = '?', type = str, help = 'Minimum query timestamp', default = "infer")#2019-04-01T00:00:00
    parser.add_argument('--n_it', nargs = '?', type = int, help = 'Minimum number of iterations', default = default_n_iter  )
    parser.add_argument('--timeout', nargs = '?', type = float, help = 'Query execution timeout in seconds', default = default_timeout)
    parser.add_argument('--additional_arguments', nargs = '?', type = str, help = 'Additional arguments to be passed to the scripts', default = '')
    args = parser.parse_args()
    
    # if args.max_ts == "infer" or args.min_ts  == "infer":
    #
    #     from systems.utils import get_start_and_stop_dates
    #
    #     start, stop = get_start_and_stop_dates(args.datasets[0])
    #     if args.min_ts  == "infer":
    #          args.min_ts = start
    #     if args.max_ts == "infer":
    #         args.max_ts = stop
            
    return args
