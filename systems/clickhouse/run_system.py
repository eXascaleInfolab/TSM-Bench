import random
import sys
from clickhouse_driver import connect as connect_ClickHouse
from subprocess import Popen, PIPE, STDOUT, DEVNULL

# setting path
sys.path.append('../..')
from systems.utils import change_directory , parse_args , connection_class

def get_connection(host="localhost", **kwargs):
    conn = connect_ClickHouse(f"clickhouse://{host}")
    cur = conn.cursor()
    def execute_query_f(sql):
        cur.execute(sql)
        return cur.fetchall()

    conn_close_f = lambda : conn.close()
    return connection_class.Connection(conn_close_f, execute_query_f)

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
    query = query.replace("<sid1>", "s1")
    query = query.replace("<sid2>", "s2")

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

