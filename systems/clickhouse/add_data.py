from threading import Event

import psycopg2
import time

from clickhouse_driver import Client
from clickhouse_driver import connect as connect_ClickHouse
from utils.online_computer import IngestionResult


def generate_insertion_query(time_stamps : list , station_ids : list , sensors_values , dataset):
    template_start = f"insert into {dataset} (time, id_station ," + ",".join(["s" + str(i) for i in range(100)]) + ")" + "VALUES "

    values = [ f"('{time_stamps[i]}' , '{station_ids[i]}' , {', '.join([str(s_n) for s_n in sensors_values[i]])})"
        for i,_ in enumerate(time_stamps)]

    sql = template_start + ",".join(values)
    return sql

def input_data(insertion_queries, event : Event(), ingestion_logger : IngestionResult, host = "localhost" , dataset = None ):
    ingestion_logger.set_evaluated()
    try:
        conn = connect_ClickHouse(f"clickhouse://{host}")
        cur = conn.cursor()
        for sql in insertion_queries:
            print(sql)
            if event.is_set():
                break
            start = time.time()
            cur.execute(sql)
            diff = time.time() - start
            ingestion_logger.add(100, start, time.time())
            if diff <= 1:
                time.sleep(1-diff)
            else:
                print(f"insertion to slow took {diff}s")
        ingestion_logger.set_fail(Exception("finished"))

    except Exception as e:
        ingestion_logger.set_fail(e)
        raise e
              


def delete_data(date= "2019-04-30T00:00:00", host="localhost" , dataset = "d1"):
    conn = connect_ClickHouse(f"clickhouse://{host}")
    print("cleaning up clickhouse database")
    cur = conn.cursor()
    time.sleep(4)
    res = cur.execute(f"ALTER TABLE {dataset} DELETE where time > TIMESTAMP '{date}';")
    time.sleep(10)
    print(res)