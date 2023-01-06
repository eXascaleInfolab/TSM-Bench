import argparse
import os
import sys
import subprocess

parser = argparse.ArgumentParser(description = 'Script for running any eval')
parser.add_argument('--database', nargs = '?', type = str, help = 'Database name', default = 'monetdb')
parser.add_argument('--algorithm', nargs = '?', type = str, help = 'Algorithm name', default = 'kmeans')
parser.add_argument('--dataset', nargs = '?', type = str, help = 'Dataset name or path to the file', default = 'weather')
parser.add_argument('--rows', nargs = '?', type = int, help = 'Number of rows to test', default = 100)
parser.add_argument('--columns', nargs = '?', type = int, help = 'Number of columns to test')
parser.add_argument('--additional_arguments', nargs = '?', type = str, help = 'Additional arguments to be passed to the scripts', default = '')
args = parser.parse_args()

datasets = {
	'weather': './Datasets/alabama_weather.txt',
	'activity': './Datasets/sport.txt',
	'monitoring': './Datasets/hydraulic.txt',
	'medical': './Datasets/mex_pm_01.txt',
	'WP': './Datasets/WaterPressure.txt',
	'WT' : './Datasets/WaterTemperature.txt',
	'bafu' : './Datasets/bafu.txt'
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

toRun = ['python3', 'generate_udf.py', '--file', str(args.dataset), '--rows', str(args.rows)]
if args.columns is not None:
	toRun = toRun + ['--column', str(args.columns)]
if len(args.additional_arguments) > 0:
	toRun = toRun + args.additional_arguments.split(" ")

subprocess.run(toRun)
