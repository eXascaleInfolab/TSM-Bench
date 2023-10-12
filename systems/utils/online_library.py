
import subprocess
import os
import pandas as pd
def generate_continuing_data(batch_size ,dataset):
    path_to_data_folder = "../datasets" if os.path.isdir("../datasets") else "datasets"
    data_set_name = "d1_tail.csv" 
    data_set_path =  f"{path_to_data_folder}/{data_set_name}"
    tail_process = subprocess.Popen(['tail', data_set_path, '-n', '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = tail_process.communicate()
    date , station , *sensors = stdout.decode("utf-8").strip().split(",")
    date_pd = pd.to_datetime(date)

    new_time_stamps = [ pd.to_datetime(date) + pd.Timedelta(seconds=10 * i) for i in range(1,batch_size+1)]
    print(new_time_stamps[0],new_time_stamps[-1])
    data_to_insert = f"{new_time_stamps[0].strftime('%Y-%m-%dT%H:%M:%S')},{station},{ ','.join([str(e) for e in sensors])}"
    return { "time_stamps" : [   t_s.strftime('%Y-%m-%dT%H:%M:%S') for t_s in new_time_stamps ],
         "stations" : ["st<st_id>"] * len(new_time_stamps),
         "sensors" : [sensors]* len(new_time_stamps) #sensor data
          }
