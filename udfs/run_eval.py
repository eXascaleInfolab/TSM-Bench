import argparse
import os
import sys
import subprocess
import random
import logging

logging.basicConfig(filename="test.log",format='%(message)s')
def randomize_window(dataset_file,window_size,row_size):
	dataset_name = dataset_file.split("/")[-1]
	logging.error(" ")
	logging.error("******** "+"Database: "+args.database+" | Algorithm: "+args.algorithm+" | Dataset : "+dataset_name+" | Window Size: "+str(window_size)+" | Row Size: "+str(row_size)+" ********")
	
	f = open(dataset_file, "r")
	

	if window_size>row_size: #checks to see if window specified is greater than lines specified.
	        logging.error("Invalid window. Please restart program")
	        f.close()
	        sys.exit("Invalid window. Please restart program")

	else:
		start_index = random.randint(0,row_size-args.window) #generates a random start index
		end_index = start_index + (window_size-1)
		logging.error("Start Index: "+str(start_index)+" | End Index: "+str(end_index))
		for i in range(end_index+1):
			line = f.readline()
			if line == '' :
				logging.error("File too small. Please use a lesser number of rows.")
				f.close()
				sys.exit("File too small. Please use a lesser number of rows.")
			elif i==start_index:
				start_time = line.split(" ")[0]
			elif i==end_index:
				end_time = line.split(" ")[0]

		f.close()
		return start_time, end_time

parser = argparse.ArgumentParser(description = 'Script for running any eval')
parser.add_argument('--database', nargs = '?', type = str, help = 'Database name', default = 'monetdb')
parser.add_argument('--algorithm', nargs = '?', type = str, help = 'Algorithm name', default = 'kmeans')
parser.add_argument('--dataset', nargs = '?', type = str, help = 'Dataset name or path to the file', default = 'weather')
parser.add_argument('--rows', nargs = '?', type = int, help = 'Number of rows to test', default = 100)
parser.add_argument('--percentage', nargs = '?', type = int, help = 'Window of items to test', default = 10)
parser.add_argument('--columns', nargs = '?', type = int, help = 'Number of columns to test')
#parser.add_argument('--export', nargs = '*', type = str, help = 'Path to file where to export the results', default = 'results.txt')
parser.add_argument('--additional_arguments', nargs = '?', type = str, help = 'Additional arguments to be passed to the scripts', default = '')
args = parser.parse_args()


datasets = {
	'weather': './Datasets/alabama_weather.txt',
	'activity': './Datasets/sport.txt',
	'monitoring': './Datasets/hydraulic.txt',
	'medical': './Datasets/mex_pm_01.txt',
	'synthetic': './Datasets/synthetic.txt',
	'bafu': './Datasets/bafu.txt',
	'WP' : 'Datasets/Water_Pressure.txt',
	'WT' : 'Datasets/Water_Temperature.txt',
	'WP_s' : 'Datasets/Water_Pressure_s.txt',
	'WT_s' : 'Datasets/Water_Temperature_s.txt'
}


if args.dataset in datasets:
	args.dataset = datasets[args.dataset]
if not(os.path.exists(args.dataset)):
	sys.exit("Invalid dataset file: " + args.dataset)
args.dataset = os.path.abspath(args.dataset)

databasePath = os.path.join(os.getcwd(), "Databases", args.database)
if not(os.path.exists(databasePath)):
	sys.exit("Invalid database: " + args.database)

evalPath = os.path.join(databasePath, args.algorithm)
if not(os.path.exists(evalPath)):
	sys.exit("Invalid algorithm: " + args.algorithm)
os.chdir(evalPath)

args.window = int(args.rows * args.percentage / 100)

start_time,end_time = randomize_window(args.dataset,args.window,args.rows)
logging.error("Start Time: "+str(start_time)+" | End Time: "+str(end_time))

toRun = ['python3', 'generate_udf.py', '--file', str(args.dataset), '--rows', str(args.rows),'--start_time',str(start_time),'--end_time',str(end_time)]
if args.columns is not None:
	toRun = toRun + ['--column', str(args.columns)]
#if args.columns is not None:
#	toRun = toRun + ['--export', str(args.export)]
if len(args.additional_arguments) > 0:
	toRun = toRun + args.additional_arguments.split(" ")

subprocess.run(toRun)
