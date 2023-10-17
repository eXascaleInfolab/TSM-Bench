import jsonlines

STORE_GLOBALS = {"mode" : "offline", "dataset" : None} #keep the default here as offline 

def set_offline():
    STORE_GLOBALS["mode"] = "offline"
    
def set_online():
    STORE_GLOBALS["mode"] = "online"

def set_dataset(dataset):
    STORE_GLOBALS["dataset"] = dataset

def store(system_name, *, runtime, var, n_stations, n_sensors, time_range, query, original_query=None, results_path="../../results"):
    # Create a dictionary to store the data
    data = {
        "system_name": system_name,
        "runtime": runtime,
        "var": var,
        "n_stations": n_stations,
        "n_sensors": n_sensors,
        "time_range": time_range,
        "query": query,
        "dataset" : STORE_GLOBALS["dataset"]
    }

    if original_query is not None:
        data["original_query"] = original_query

    # Define the path to the JSONL file (adjust the path as needed)
    jsonl_file = f"{results_path}/{STORE_GLOBALS['mode']}_data.jsonl"

    # Append the data to the JSONL file
    with jsonlines.open(jsonl_file, mode='a') as writer:
        writer.write(data)