import psycopg2
import time



def generate_insertion_query(time_stamps : list , station_ids : list , sensors_values , dataset):
    template_start = f"insert into {dataset} (time, id_station ," + ",".join(["s" + str(i) for i in range(100)]) + ")" + "VALUES "

    values = [ f"('{time_stamps[i]}' , '{station_ids[i]}' , {', '.join([str(s_n) for s_n in sensors_values[i]])})"
        for i,_ in enumerate(time_stamps)]

    sql = template_start + ",".join(values)
    return sql



def input_data(insertion_queries, event , ingestion_logger , host = "localhost" , dataset = None ):
    ingestion_logger.set_evaluated()
    try:
        CONNECTION = f"postgres://postgres:postgres@{host}:5432/postgres"
        conn = psycopg2.connect(CONNECTION)
        conn.autocommit = True
        cur = conn.cursor()
        for sql in insertion_queries:
            if event.is_set():
                break
            start = time.time()
            cur.execute(sql)
            diff = time.time() - start
            ingestion_logger.add(100, start, time.time())
            if diff < 1:
                time.sleep(1-diff)
            else:
                print(f"insertion to slow took {diff}s")
    except:
        results["status"] = "failed"


def delete_data(date="2019-04-1 00:00:00", host = "localhost", dataset = "d1"):
    CONNECTION = f"postgres://postgres:postgres@{host}:5432/postgres"
    conn = psycopg2.connect(CONNECTION)
    conn.autocommit = True
    print("cleaning up the timescale database")
    start = time.time()
    sql = f"SELECT drop_chunks('{dataset}', newer_than => '{date}');"
    print(sql)
    cur = conn.cursor()
    result = cur.execute(sql)
    print(result)