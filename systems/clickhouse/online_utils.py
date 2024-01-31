from clickhouse_driver import connect as connect_ClickHouse

def generate_insertion_query(time_stamps: list, station_ids: list, sensors_values, dataset):
    template_start = f"insert into {dataset} (time, id_station ," + ",".join(
        ["s" + str(i) for i in range(100)]) + ")" + " VALUES "

    values = [f"('{time_stamps[i]}' , '{station_ids[i]}' , {', '.join([str(s_n) for s_n in sensors_values[i]])})"
              for i, _ in enumerate(time_stamps)]

    sql = template_start + ",".join(values)
    return sql


def delete_data(date="2019-04-30T00:00:00", host="localhost", dataset="d1"):
    conn = connect_ClickHouse(f"clickhouse://{host}")
    print("cleaning up clickhouse database")
    cur = conn.cursor()
    res = cur.execute(f"ALTER TABLE {dataset} DELETE where time > TIMESTAMP '{date}';")
    print(res)
