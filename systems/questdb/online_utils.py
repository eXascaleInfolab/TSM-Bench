import psycopg2
import time

def generate_insertion_query(time_stamps: list, station_ids: list, sensors_values, dataset):
    template_start = f"insert into {dataset} (ts, id_station ," + ",".join(
        ["s" + str(i) for i in range(100)]) + ")" + " VALUES "

    values = [f"('{time_stamps[i]}' , '{station_ids[i]}' , {', '.join([str(s_n) for s_n in sensors_values[i]])})"
              for i, _ in enumerate(time_stamps)]

    sql = template_start + ",".join(values)
    return sql

def delete_data(date= "2019-04-30T00:00:00", host = "localhost", dataset = "d1"):
    print("cleaning up questdb")
    conn = psycopg2.connect(user="admin",
          password="quest",
          host=host,
          port="8812",
          database="d1")
    start = time.time()
    cur = conn.cursor()
    sql = f"""drop table if exists table_copy; """
    sql = f"""create table table_copy as (select * from {dataset} where ts < '{date}') timestamp (ts) PARTITION BY DAY; """
    cur.execute(sql)
    cur.execute(f"drop table {dataset};")
    cur.execute(f"rename table table_copy to {dataset};")
