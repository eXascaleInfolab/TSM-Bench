

import os
import pandas as pd
def generate_continuing_data(batch_size = 100000):
	path_to_data_folder = "../datasets" if os.path.isdir("../datasets") else "datasets"
	data_set_name = "d1_tail.csv" 
	data_set_path =  f"{path_to_data_folder}/{data_set_name}"

	date , station , *sensors = pd.read_csv(data_set_path).values[-1,:]
	date_pd = pd.to_datetime(date)

	new_time_stamps = [ pd.to_datetime(date) + pd.Timedelta(seconds=10 * i) for i in range(1,batch_size+1)]
	print(new_time_stamps[0],new_time_stamps[-1])
	data_to_insert = f"{new_time_stamps[0].strftime('%Y-%m-%dT%H:%M:%S')},{station},{ ','.join([str(e) for e in sensors])}"
	return { "time_stamps" : [   t_s.strftime('%Y-%m-%dT%H:%M:%S') for t_s in new_time_stamps ],
		 "stations" : ["st<st_id>"] * len(new_time_stamps),
		 "sensors" : [sensors]* len(new_time_stamps) #sensor data
		}
