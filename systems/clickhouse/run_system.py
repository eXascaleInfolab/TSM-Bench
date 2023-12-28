from datetime import datetime
from tqdm import tqdm
import time
import statistics as stats
import random
import sys
from clickhouse_driver import connect as connect_ClickHouse
from subprocess import Popen, PIPE, STDOUT, DEVNULL

# setting path
sys.path.append('../..')
from systems.utils.library import get_randomized_inputs
from systems.utils import change_directory , parse_args
from utils.run_systems import run_system

def launch():
    with change_directory(__file__):
        process = Popen(['sh', 'launch.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

        process = Popen(['sleep', '10'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

def stop():
    with change_directory(__file__):
        process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

def get_query_exec_f_and_conn_close_f(host="localhost", **kwargs):
    conn = connect_ClickHouse(f"clickhouse://{host}")
    cur = conn.cursor()
    def execute_query_f(sql):
        cur.execute(sql)
        return cur.fetchall()

    conn_close_f = lambda : conn.close()
    return execute_query_f, conn_close_f


def parse_query(query ,*,  date, rangeUnit , rangeL , sensor_list , station_list):
    query = query.replace("<timestamp>", date)
    query = query.replace("<range>", str(rangeL))
    query = query.replace("<rangesUnit>", rangeUnit)

    # sensors
    q = sensor_list[0]
    q_filter = '(' + sensor_list[0] + ' > 0.95' + ')'
    q_avg = 'avg(' + sensor_list[0] + ')'
    for j in sensor_list[1:]:
        q += ', ' + j
        q_avg += ', ' + 'avg(' + j + ')'

    query = query.replace("<sid>", q)
    query = query.replace("<sfilter>", q_filter)
    query = query.replace("<avg_s>", q_avg)
    query = query.replace("<sid1>", "1")
    query = query.replace("<sid2>", "2")

    if "fill step" in query.lower():
        if len(station_list) == 1:
            q = "('" + 'st' + str(random.sample(range(10), 1)[0]) + "')"
            query = query.replace("<stid>", q)

        else:
            fill_commands = []  # queries to unite
            for station in station_list:
                q = f"('{station}')"
                station_fill = query.replace("<stid>", q).replace(";", "")
                fill_commands.append(station_fill)

            query = "SELECT * FROM (" + " UNION ALL ".join(fill_commands) + ")"

    else:  # normal station insertion
        q = "(" + ', '.join(["'" + j + "'" for j in station_list]) + ")"
        query = query.replace("<stid>", q)

    return query

def run_query(query, rangeL ,rangeUnit ,n_st ,n_s ,n_it , dataset,  host="localhost"):

    # Connect to the system
    conn = connect_ClickHouse(f"clickhouse://{host}",port=9000)
    cursor = conn.cursor()#cursor = Client(host='localhost',port=9001)

    random_inputs = get_randomized_inputs(dataset ,n_st = n_st ,n_s = n_s , n_it =  n_it , rangeL = rangeL )
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

        query = parse_query(query, date=date, rangeUnit = rangeUnit , rangeL = rangeL , sensor_list = sensor_list ,station_list=station_list)
        print("query")
        start = time.time()
        
        cursor.execute(query)
        cursor.fetchall()
        
        diff = (time.time()-start)*1000
        runtimes.append(diff)
        if time.time() - full_time > 200 and it > 5:
            break  

    conn.close()
    return stats.mean(runtimes), stats.stdev(runtimes)

if __name__ == "__main__":
    launch()
    
    args = parse_args() 
    
    def query_f(query, rangeL = args.range, rangeUnit = args.rangeUnit,
                n_st = args.def_st, n_s = args.def_s, n_it = args.n_it, dataset = args.dataset):
        return run_query(query, rangeL=rangeL, rangeUnit = rangeUnit ,n_st = n_st , n_s = n_s , n_it = n_it , dataset = dataset)
    
    run_system(args,"clickhouse",query_f)

    stop()
