
import subprocess
import os
import pandas as pd

def generate_continuing_data(batch_size ,dataset):
    from systems.utils import get_start_and_stop_dates

    _ , date_pd = get_start_and_stop_dates(dataset)

    new_time_stamps = [ pd.to_datetime(date_pd) + pd.Timedelta(seconds=10 * i) for i in range(1,batch_size+1)]
    # print(new_time_stamps[0],new_time_stamps[-1])
    data_to_insert = f"{new_time_stamps[0].strftime('%Y-%m-%dT%H:%M:%S')},{0},{ ','.join([str(e) for e in range(100)])}"
    return { "time_stamps" : [   t_s.strftime('%Y-%m-%dT%H:%M:%S') for t_s in new_time_stamps ],
         "stations" : ["st<st_id>"] * len(new_time_stamps),
         "sensors" : [sensors]* len(new_time_stamps) #sensor data
          }
