from systems.utils import get_randomized_inputs
import time
import statistics as stats
from systems.utils.connection_class import Connection
from tqdm import tqdm


def run_query(system_module, query_template,  rangeL, rangeUnit, n_st, n_s, n_it, dataset, host="localhost",log=False):
    # Connect to the system
    client : Connection = system_module.get_connection(host=host,dataset=dataset)

    random_inputs = get_randomized_inputs(dataset, n_st=n_st, n_s=n_s, n_it=n_it, rangeL=rangeL)
    random_stations = random_inputs["stations"]
    random_sensors = random_inputs["sensors"]
    random_sensors_dates = random_inputs["dates"]

    runtimes = []
    full_time = time.time()

    for it in tqdm(range(n_it)):
        date = random_sensors_dates[it]
        sensor_list = random_sensors[it]
        station_list = random_stations[it]

        assert len(sensor_list) == n_s
        assert len(station_list) == n_st
        assert type(date) == str

        query = system_module.parse_query(query_template, date=date, rangeUnit=rangeUnit, rangeL=rangeL, sensor_list=sensor_list,
                            station_list=station_list)
        if log:
            print("query")
            print(query)

        start = time.time()
        client.execute(query)
        # print("done querying")
        diff = (time.time() - start) * 1000
        runtimes.append(diff)
        if time.time() - full_time > 200 and it > 5:
            break

    client.close()
    return round(stats.mean(runtimes), 3), round(stats.stdev(runtimes), 3)