import sys
import pandas as pd
import json

from subprocess import Popen, PIPE, STDOUT, DEVNULL  # py3k

# setting path
sys.path.append('../../')
from systems.utils.library import *
from systems.utils import change_directory, parse_args, connection_class
from utils.run_systems import run_system

import pymonetdb

def get_connection(host="localhost", **kwargs):
    conn = pymonetdb.connect(username="monetdb", port=54320, password="monetdb", hostname=host, database="mydb")
    cursor = conn.cursor()
    # isolation_level = "SERIALIZABLE"  # For the online queries
    # cursor.execute(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}")

    def execute_query_f(sql):
        cursor.execute(sql)
        return cursor.fetchall()

    def write_query_f(sql):
        return cursor.execute(sql)

    conn_close_f = lambda : conn.close()
    return connection_class.Connection(conn_close_f, execute_query_f,write_query_f)


def parse_query(query, *, date, rangeUnit, rangeL, sensor_list, station_list):
    if rangeUnit in ["week", "w", "WEEK"]:
        rangeUnit = "day"
        rangeL = rangeL * 7

    temp = query.replace("<timestamp>", date)
    temp = temp.replace("<range>", str(rangeL))
    temp = temp.replace("<rangesUnit>", rangeUnit)

    # stations
    q = "(" + "'" + station_list[0] + "'"
    for j in station_list[1:]:
        q += ', ' + "'" + j + "'"
    q += ")"

    temp = temp.replace("<stid>", q)
    stid1 = station_list[0]
    stid2 = "" + station_list[1] + "" if len(station_list) > 1 else "st0"
    temp = temp.replace("<stid1>", stid1)
    temp = temp.replace("<stid2>", stid2)

    # sensors
    q = sensor_list[0]
    q_filter = '(' + sensor_list[0] + ' > 0.95'
    q_avg = 'avg(' + sensor_list[0] + ')'
    for j in sensor_list[1:]:
        q += ', ' + j
        # q_filter += ' OR ' + j + ' > 0.95'
        q_avg += ', ' + 'avg(' + j + ')'

    temp = temp.replace("<sid>", q)
    sid1 = sensor_list[0]
    sid2 = sensor_list[1] if len(sensor_list) > 1 else "s2"
    sid3 = sensor_list[2] if len(sensor_list) > 3 else "s3"
    temp = temp.replace("<sid1>", sid1)
    temp = temp.replace("<sid2>", sid2)
    temp = temp.replace("<sid3>", sid3)
    temp = temp.replace("<sfilter>", q_filter + ')')
    temp = temp.replace("<avg_s>", q_avg)

    import re
    # match a=(b,c,...) make it a=b or a=c or ...
    equality_missmatches = re.findall(r"\b\w+\s*=\s*\([^)]*?,[^)]*?\)", temp)
    for equality_missmatch in equality_missmatches:
        pattern, options = equality_missmatch.split("=")
        options = options.replace(")", "").replace("(", "").split(",")
        res = "(" + " or ".join([pattern + "= " + o for o in options]) + ")"
        temp = temp.replace(equality_missmatch, res)

    return temp


def run_query(query, rangeL, rangeUnit, n_st, n_s, n_it, dataset, host="localhost"):
    # Connect to the system
    conn = pymonetdb.connect(username="monetdb", port=54320, password="monetdb", hostname=host, database="mydb")
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

        start = time.time()
        cursor.execute(query)
        cursor.fetchall()

        diff = (time.time() - start) * 1000
        runtimes.append(diff)
        if time.time() - full_time > 200 and it > 5:
            break

    conn.close()
    return stats.mean(runtimes), stats.stdev(runtimes)


def launch():
    print("launching monetdb")
    with change_directory(__file__):
        process = Popen(['sh', 'launch.sh', '&'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

        process = Popen(['sleep', '2'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()


def stop():
    with change_directory(__file__):
        process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()


if __name__ == "__main__":
    args = parse_args()

    launch()
    def query_f(query, rangeL=args.range, rangeUnit=args.rangeUnit, n_st=args.def_st, n_s=args.def_s, n_it=args.n_it):
        return run_query(query, rangeL=rangeL, rangeUnit=rangeUnit, n_st=n_st, n_s=n_s, n_it=n_it)

    run_system(args, "monetdb", query_f)

    stop()
