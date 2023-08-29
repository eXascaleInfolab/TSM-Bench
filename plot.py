import os
import sys
from pygnuplot import gnuplot
import pygnuplot
import pandas as pd

import matplotlib.pyplot as plt


results_folder = "results"
import tempfile

data_set = "d1"
data_set_folder = f"{results_folder}/{data_set}"

queries = sorted(os.listdir(data_set_folder))

import argparse 

parser = argparse.ArgumentParser(description='Query intput.')

parser.add_argument("--query", "-q",type=int,nargs="?", default=1)
parser.add_argument("--store", "-s",type=int,nargs="?",default=1)
args = parser.parse_args()


try:
	selected_query = [ q for q in  queries  if q.endswith(str(args.query))][0]
except IndexError :
	print(f"query: {args.query} not found, possible queries: {queries}")
	

query_dir = f"{data_set_folder}/{selected_query}"
db_txt_files = sorted([ f_name for f_name in os.listdir(query_dir) if f_name.endswith(".txt")])

results = { file_n.split(".")[0] :  pd.read_csv(query_dir+"/"+file_n,index_col=0) for file_n in db_txt_files}

## splits scenarios 

stations_scenario = { k : df[df.index.str.contains('st_')][["runtime"]] for k,df in results.items() }

sensor_scenario = { k :df[df.index.str.contains('s_')][["runtime"]] for k,df in results.items() }

time_scenario = { k : df[~df.index.str.contains('_')][["runtime"]] for k,df  in results.items() }

combined_df = pd.concat([df.rename(columns={'runtime': key}) for key, df in stations_scenario.items()], axis=1)
print(combined_df)
import matplotlib_terminal



combined_df.plot()
plt.title(f"{selected_query} varying #stations")
plt.savefig(f"{query_dir}/stations.png")
plt.show('gamma') # Use RendererGamma-fast/noblock from img2unicode renderer
plt.close()




combined_df = pd.concat([df.rename(columns={'runtime': key}) for key, df in sensor_scenario.items()], axis=1)
print(combined_df)
combined_df.plot()
plt.title(f"{selected_query} varying #sensors")
plt.savefig(f"{query_dir}/sensors.png")
plt.show('gamma') # Use RendererGamma-fast/noblock from img2unicode renderer
plt.close()



combined_df = pd.concat([df.rename(columns={'runtime': key}) for key, df in time_scenario.items()], axis=1)

combined_df.plot()
plt.title(f"{selected_query} varying time range")
plt.savefig(f"{query_dir}/time_range.png")
plt.show('gamma') # Use RendererGamma-fast/noblock from img2unicode renderer
plt.close()

