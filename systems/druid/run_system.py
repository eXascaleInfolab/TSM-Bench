import sys
import time
import statistics as stats
from tqdm import tqdm
from subprocess import Popen, PIPE, STDOUT, DEVNULL

from pydruid.client import *
from pydruid.db import connect
from pydruid.utils.aggregators import *
from pydruid.utils.filters import *
from pydruid.db.exceptions import ProgrammingError

# setting path
sys.path.append('../../')
from systems.utils.library import *
from systems.utils import change_directory, connection_class


def get_connection(host="localhost", dataset=None , **kwargs):
    conn = connect(host=host, port=8082, path='/druid/v2/sql/', scheme='http')
    cursor = conn.cursor()
    def execute_query_f(sql):
        cursor.execute(sql)
        return cursor.fetchall()

    def write_points_f(points ,dataset=dataset):
        raise NotImplementedError("druid does not support insertion")

    conn_close_f = lambda : conn.close()
    return connection_class.Connection(conn_close_f, execute_query_f, write_points_f)



def parse_query(query, *, date, rangeUnit, rangeL, sensor_list, station_list):
    date = date.replace("T", " ")
    temp = query.replace("<timestamp>", date)
    temp = temp.replace("<range>", str(rangeL))
    temp = temp.replace("<rangesUnit>", rangeUnit)

    # stations
    q = "(" + "'" + station_list[0] + "'"
    for j in station_list[1:]:
        q += ', ' + "'" + j + "'"
    q += ")"
    temp = temp.replace("<stid>", q)

    # sensors
    q = sensor_list[0]
    q_filter = '(' + sensor_list[0] + ' > 0.95'
    q_avg = 'avg(' + sensor_list[0] + ')'
    for j in sensor_list[1:]:
        q += ', ' + j
        q_avg += ', ' + 'avg(' + j + ')'

    temp = temp.replace("<sid>", q)
    temp = temp.replace("<sid1>", sensor_list[0])
    sid2 = sensor_list[1] if len(sensor_list) > 1 else "s2"
    sid3 = sensor_list[2] if len(sensor_list) > 2 else "s3"
    temp = temp.replace("<sid2>", sid2)
    temp = temp.replace("<sid3>", sid3)
    temp = temp.replace("<sfilter>", q_filter + ')')
    temp = temp.replace("<avg_s>", q_avg)

    return temp


def run_query(query, rangeL, rangeUnit, n_st, n_s, n_it, dataset, host="localhost"):
    if rangeUnit in ["week", "w", "Week"]:
        rangeUnit = "day"
        rangeL = rangeL * 7

    # Connect to the system
    conn = connect(host=host, port=8082, path='/druid/v2/sql/', scheme='http')
    cursor = conn.cursor()
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

        query = parse_query(query, date=date, rangeUnit=rangeUnit, rangeL=rangeL, sensor_list=sensor_list,
                            station_list=station_list)
        print("query")
        start = time.time()

        try:
            cursor.execute(query)
            results_ = cursor.fetchall()
        except ProgrammingError as e:
            print("Exception:", e)
            print("Skipping this query due to resource limit exceeded.")
            continue

        diff = (time.time() - start) * 1000
        #  print(temp, diff)
        runtimes.append(diff)
        if time.time() - full_time > 500 and it > 2:
            break

    conn.close()
    return stats.mean(runtimes), stats.stdev(runtimes)


def launch():
    print("launching druid")

    with change_directory(__file__):
        process = Popen(['sh', 'launch.sh', '&'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()  # launch.sh  from druid has to sleep for long itself

    print("druid launched")


def stop():
    with change_directory(__file__):
        process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()
