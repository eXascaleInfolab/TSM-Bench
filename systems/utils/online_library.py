import os
import pandas as pd
import json
import numpy as np
def generate_continuing_data(batch_size, dataset , stop_date_pd=None):
    """
    :param batch_size: number of data rows to generate
    :param dataset: dataset name
    :param stop_date_pd: pandas date after which to append new data
    :return: dict with keys: time_stamps, stations, sensors, new_stop_date, start_date
    sensors are uniformly distributed between 0 and 1
    stations are randomly chosen from the number of available stations
    time_stamps are 10 seconds apart

    """

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
            "stations": [f"st{np.random.choice(n_stations_total)}" for i , _ in enumerate(new_time_stamps)],
            "sensors" : [list(np.random.random(n_sensors_total)) for i , _ in enumerate(new_time_stamps)],
            "new_stop_date" : new_time_stamps[-1],
            "start_date" : time_start
            }
