import argparse
# Parse Arguments

def run_parser(*,default_n_iter=100, default_timeout=20):
    parser = argparse.ArgumentParser(description = 'Script for running any eval')
    parser.add_argument('--datasets', nargs = '*', type = str, help = 'Dataset name', default = 'd1')
    parser.add_argument('--queries', nargs = '?', type = str, help = 'List of queries to run (Q1-Q7)', default = "q1 q2 q3 q4 q5 q6 q7")
    parser.add_argument('--nb_st', nargs = '?', type = int, help = 'Number of stations in the dataset', default = 10)
    parser.add_argument('--nb_s', nargs = '?', type = int, help = 'Number of sensors in the dataset', default = 100)
    parser.add_argument('--def_st', nargs = '?', type = int, help = 'Default number of queried stations', default = 1)
    parser.add_argument('--def_s', nargs = '?', type = int, help = 'Default number of queried sensors', default = 3)
    parser.add_argument('--range', nargs = '?', type = int, help = 'Query range', default = 1)
    parser.add_argument('--rangeUnit', nargs = '?', type = str, help = 'Query range unit', default = 'day')
    parser.add_argument('--max_ts', nargs = '?', type = str, help = 'Maximum query timestamp', default = "2019-04-30 00:00:00")
    parser.add_argument('--min_ts', nargs = '?', type = str, help = 'Minimum query timestamp', default = "2019-04-01 00:00:00")
    parser.add_argument('--timeout', nargs = '?', type = float, help = 'Query execution timeout in seconds', default = default_timeout)
    parser.add_argument('--n_it', nargs = '?', type = int, help = 'Minimum number of iterations', default = default_n_iter)
    parser.add_argument('--additional_arguments', nargs = '?', type = str, help = 'Additional arguments to be passed to the scripts', default = '')
    args = parser.parse_args()
    return args