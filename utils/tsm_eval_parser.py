import argparse
import sys

def init_main_parser(system_names , datasets , defualt_iter ):
    parser = argparse.ArgumentParser(description='Script for running any eval')
    parser.add_argument('--systems', nargs='+', type=str, help='Systems name', default=['clickhouse'],
                        choices=system_names + ["all"])
    parser.add_argument('--datasets', nargs='*', type=str, help='Dataset name', default=['d1'])
    parser.add_argument('--queries', nargs='*', type=str, help='List of queries to run (Q1-Q7)',
                        default="q1 q2 q3 q4 q5 q6 q7")
    parser.add_argument('--n_st', nargs='?', type=int, help='Number of stations in the dataset', default=10)
    parser.add_argument('--n_s', nargs='?', type=int, help='Number of sensors in the dataset', default=100)
    parser.add_argument('--nb_st', nargs='?', type=int, help='Default number of queried stations', default=1)
    parser.add_argument('--nb_sr', nargs='?', type=int, help='Default number of queried sensors', default=3)
    parser.add_argument('--n_it', nargs='?', type=int, help='Default number of queried sensors', default=defualt_iter)
    parser.add_argument('--range', nargs='?', type=str, help='Query range', default="1day")
    parser.add_argument('--timeout', nargs='?', type=str, help='Query execution timeout in seconds', default=200)
    parser.add_argument('--additional_arguments', nargs='?', type=str,
                        help='Additional arguments to be passed to the scripts', default='')
    args = parser.parse_args()

    try:
        index = 0
        while index < len(args.range) and args.range[index].isdigit():
            index += 1
        args.rangeUnit = args.range[index:]
        args.range = int(args.range[:index])
    except:
        print("Input string does not conform to the expected format.", args.rangeUnit.upper())
        args.range = 1
        args.rangeUnit = "day"

    if args.systems[0] == "all":
        args.systems = system_names

    if "all" in args.queries:
        args.queries = "q1,q2,q3,q4,q5,q6,q7"

    if args.datasets == 'all':
        args.datasets = ['d1', 'd2']

    args.queries = args.queries if "," not in args.queries else args.queries.split(",")

    try:
        args.systems = args.systems.split()
    except:
        pass

    for d in args.datasets:
        if d not in datasets:
            sys.exit("Invalid dataset name: " + args.datasets)

    return args