import psycopg2
import time

def generate_insertion_query(time_stamps : list , station_ids : list , sensors_values , dataset):
    template_start = f"insert into {dataset} (time, id_station ," + ",".join(["s" + str(i) for i in range(100)]) + ")" + "VALUES "

    values = [ f"('{time_stamps[i]}' , '{station_ids[i]}' , {', '.join([str(s_n) for s_n in sensors_values[i]])})"
        for i,_ in enumerate(time_stamps)]

    sql = template_start + ",".join(values)
    return sql


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