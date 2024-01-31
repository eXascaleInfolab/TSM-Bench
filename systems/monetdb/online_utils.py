
import pymonetdb
import time

conn = None


def generate_insertion_query(time_stamps: list, station_ids: list, sensors_values, dataset):
    template_start = f"insert into {dataset} (time, id_station ," + ",".join(
        ["s" + str(i) for i in range(100)]) + ")" + " VALUES "

    values = [f"('{time_stamps[i]}' , '{station_ids[i]}' , {', '.join([str(s_n) for s_n in sensors_values[i]])})"
              for i, _ in enumerate(time_stamps)]

    sql = template_start + ",".join(values)
    return sql

def delete_data(date= "2019-04-1 00:00:00", host = "localhost", dataset = "d1"):
    conn = pymonetdb.connect(username="monetdb", port=54320, password="monetdb", hostname=host, database="mydb", autocommit = True)
    print("cleaning up monetdb database")
    cur = conn.cursor()
    time.sleep(10) # concurrency safety
    res = cur.execute(f"DELETE from {dataset} where time > TIMESTAMP '{date}';")
