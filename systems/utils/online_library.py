import os
import pandas as pd
import json
import numpy as np
def generate_continuing_data(batch_size, dataset , stop_date_pd=None):
    path_to_data_folder = "../../datasets" if os.path.isdir("../../datasets") else "datasets"
    with open(f"{path_to_data_folder}/dataset_config.json") as f:
        dataset_config = json.load(f)[dataset]

    n_sensors_total = dataset_config["n_sensors"]
    n_stations_total = dataset_config["n_stations"]
    time_start, time_stop = dataset_config["time_start_stop"]

    if stop_date_pd is None:
        stop_date_pd = pd.to_datetime(time_stop)

    new_time_stamps = [pd.to_datetime(stop_date_pd) + pd.Timedelta(seconds=10 * i) for i in range(1, batch_size + 1)]

    return {"time_stamps": [t_s.strftime('%Y-%m-%dT%H:%M:%S') for t_s in new_time_stamps],
            "stations": [f"st{i%n_stations_total}" for i , _ in enumerate(new_time_stamps)],
            "sensors" : [list(np.random.random(100)) for i , _ in enumerate(new_time_stamps)],
            "new_stop_date" : new_time_stamps[-1],
            "start_date" : time_start
            }
