import json
import sys

import pandas as pd
import os
import numpy as np



def generate_continuing_data(batch_size, dataset, stop_date_pd=None):
    """
    :param batch_size: number of data rows to generate
    :param dataset: dataset name
    :param stop_date_pd: pandas date after which to append new data
    :return: dict with keys: time_stamps, stations, sensors, new_stop_date, start_date
    sensors are uniformly distributed between 0 and 1
    stations are randomly chosen from the number of available stations
    time_stamps are 10 seconds apart
    """
    from utils.dataset_config_reader import get_dataset_infos

    dataset_config = get_dataset_infos(dataset)

    n_sensors_total = dataset_config["n_sensors"]
    n_stations_total = dataset_config["n_stations"]
    time_start, time_stop = dataset_config["time_start"] , dataset_config["time_stop"]

    if stop_date_pd is None:
        stop_date_pd = pd.to_datetime(time_stop)

    new_time_stamps = [pd.to_datetime(stop_date_pd) + pd.Timedelta(seconds=10 * i) for i in range(1, batch_size + 1)]

    for i, t_s in enumerate(new_time_stamps):
        yield {"time_stamp": t_s.strftime('%Y-%m-%dT%H:%M:%S'),
               "station": f"st{np.around(np.random.choice(n_stations_total),decimals=4)}",
               "sensor_values": list(np.random.random(n_sensors_total)),
               }


def ingestion_queries_generator(system,*,n_rows_s, t_n):
    """
    :param system: system name
    :param t_n: thread number
    :return: list of ingestion queries
    """

    folder_path = f"utils/ingestion/ingestion_queries"
    file_path = f"{folder_path}/queries_{system}_{n_rows_s}_{t_n}.txt"
    queries_line_indices = []
    print(os.getcwd())
    with open(file_path, 'r') as file:
        offset = 0
        for line in file:
            queries_line_indices.append(offset)
            offset += len(line)

        # Yield each line from the file, opening and closing the file each time
    for offset in queries_line_indices:
        with open(file_path, 'r') as file:
            file.seek(offset)
            if system == "influx" or system == "influxdb":
                points = file.readline().strip().split(";")
                yield points
            else:
                yield file.readline().strip()


def generate_ingestion_queries(*, n_threads, n_rows_s, max_runtime, dataset, system, insertion_query_f):
    """

    :param n_threads: number of threads
    :param n_rows_s:  number of rows per ingestion query
    :param max_runtime: maximum runtime in seconds
    :param dataset: dataset name
    :param system:  system name
    :param insertion_query_f: function to generate ingestion query for the system
    :return:
    """

    insertion_queries_generators = [-1] * n_threads
    for t_n in range(n_threads):
        folder_path = f"utils/ingestion/ingestion_queries"
        os.makedirs(folder_path, exist_ok=True)
        file_path = f"utils/ingestion/ingestion_queries/queries_{system}_{n_rows_s}_{t_n}.txt"
        skip = False
        if os.path.isfile(file_path):
            print(f"file queries_{system}_{t_n}.txt already exists")
            # check if file has n_rows_s lines
            with open(file_path, "r") as f:
                n_lines = sum(1 for _ in f)
            if n_lines >= max_runtime:
                skip = True
            else:
                with open(file_path, "w") as f:
                    f.write("")
            print(f"file has {n_lines} lines")

        if not skip:
            print(f"generating ingestion file queries_{system}_{n_rows_s}_{t_n}.txt")
            data_generator = generate_continuing_data(n_rows_s * max_runtime, dataset)
            for i in range(max_runtime):
                time_stamps = []
                stations = []
                sensors_values = []
                for j in range(n_rows_s):
                    data = next(data_generator)
                    time_stamps.append(data["time_stamp"])
                    stations.append(data["station"])
                    sensors_values.append(data["sensor_values"])
                ingestion_query = insertion_query_f(
                    time_stamps=time_stamps,
                    station_ids=stations,
                    sensors_values=sensors_values,
                    dataset=dataset)

                # write queries to file
                with open(file_path, "a") as f:
                    f.write(ingestion_query + "\n")

        insertion_queries_generators[t_n] = ingestion_queries_generator(system, n_rows_s=n_rows_s, t_n=t_n)

    return insertion_queries_generators


# test
# python3 utils/ingestion/ingestion_data_loading.py
if __name__ == "__main__":
    sys.path.append(os.getcwd())
    print(os.getcwd())

    system = "influx"
    dataset = "d1"
    n_threads = 2
    n_rows_s = 10
    max_runtime = 10
    from systems import influx

    insertion_query_f = influx.generate_insertion_query
    insertion_queries_generators = generate_ingestion_queries(n_threads=n_threads, n_rows_s=n_rows_s,
                                                              max_runtime=max_runtime, dataset=dataset,
                                                              system=system,
                                                              insertion_query_f=insertion_query_f)
    for t_n in range(n_threads):
        print(f"thread {t_n}")
        for i, query in enumerate(insertion_queries_generators[t_n]):
            print(query)
            if i == 100 or i == 101:
                print(query[-10:])
