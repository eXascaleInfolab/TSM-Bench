import json
import os

def get_dataset_infos(dataset):
    path_to_data_folder = "../../datasets" if os.path.isdir("../../datasets") else "datasets"

    with open(f"{path_to_data_folder}/dataset_config.json") as f:
        dataset_config = json.load(f)[dataset]

        n_sensors_total = dataset_config["n_sensors"]
        n_stations_total = dataset_config["n_stations"]
        time_start, time_stop = dataset_config["time_start_stop"]
        return {"time_start": time_start, "time_stop": time_stop, "n_sensors": n_sensors_total,
                "n_stations": n_stations_total}
