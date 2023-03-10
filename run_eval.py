import argparse
import os
import sys
import subprocess

parser = argparse.ArgumentParser(description = 'Script for running any eval')
parser.add_argument('--systems', nargs = '+', type = str, help = 'Systems name', default = 'monetdb')
parser.add_argument('--datasets', nargs = '*', type = str, help = 'Dataset name', default = 'd1')
parser.add_argument('--queries', nargs = '?', type = str, help = 'List of queries to run (Q1-Q7)', default = "q1 q2 q3 q4 q5 q6 q7")
parser.add_argument('--nb_st', nargs = '?', type = int, help = 'Number of stations in the dataset', default = 10)
parser.add_argument('--nb_s', nargs = '?', type = int, help = 'Number of sensors in the dataset', default = 100)
parser.add_argument('--def_st', nargs = '?', type = int, help = 'Default number of queried stations', default = 1)
parser.add_argument('--def_s', nargs = '?', type = int, help = 'Default number of queried sensors', default = 3)
parser.add_argument('--range', nargs = '?', type = int, help = 'Query range', default = 1)
parser.add_argument('--rangeUnit', nargs = '?', type = str, help = 'Query range unit', default = 'day')
parser.add_argument('--max_ts', nargs = '?', type = str, help = 'Maximum query timestamp', default = "2019-04-30T00:00:00")
parser.add_argument('--min_ts', nargs = '?', type = str, help = 'Minimum query timestamp', default = "2019-04-01T00:00:00")
parser.add_argument('--timeout', nargs = '?', type = str, help = 'Query execution timeout in seconds', default = 20)
parser.add_argument('--additional_arguments', nargs = '?', type = str, help = 'Additional arguments to be passed to the scripts', default = '')
args = parser.parse_args()


datasets = ['d1', 'd2']
queries = args.queries.split()
try: 
	systems = args.systems.split()
except: 
	systems = args.systems

for d in args.datasets: 	
	if d not in datasets:
		sys.exit("Invalid dataset name: " + args.dataset)

for system in systems:
	systemPath = os.path.join(os.getcwd(), "systems", system)
	if not(os.path.exists(systemPath)):
		sys.exit("Invalid system: " + system)
		
	os.chdir(systemPath)
	
	toRun = ['python3', 'run_system.py', '--datasets', ' '.join(args.datasets)
		, '--queries', str(args.queries), '--nb_st', str(args.nb_st)
		, '--nb_s', str(args.nb_s), '--range', str(args.range), '--timeout', str(args.timeout)]
		
	if len(args.additional_arguments) > 0:
		toRun = toRun + args.additional_arguments.split(" ")
	
	# print(toRun)
	subprocess.run(toRun)