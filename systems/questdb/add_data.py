import psycopg2
import time


def generate_insertion_query(time_stamps: list, station_ids: list, sensors_values, dataset):
    template_start = f"insert into {dataset} (time, id_station ," + ",".join(
        ["s" + str(i) for i in range(100)]) + ")" + " VALUES "

    values = [f"('{time_stamps[i]}' , '{station_ids[i]}' , {', '.join([str(s_n) for s_n in sensors_values[i]])})"
              for i, _ in enumerate(time_stamps)]

    sql = template_start + ",".join(values)
    return sql

def input_data(t_n, event, data , results , batch_size = 1000, host = "localhost", dataset = "d1"):
    try:
        conn = psycopg2.connect(user="admin",
          password="quest",
          host=host,
          port="8812",
          database="d1")
        cur = conn.cursor()
        data = data
        insertion_sql_head = "insert into "+dataset+" (ts, id_station ," + ",".join(["s"+str(i) for i in range(100)]) + ")"
        values = [f"('{data['time_stamps'][i]}', '{data['stations'][i]}', {', '.join([str(s_n) for s_n in data['sensors'][i]])})" for i in range(batch_size)]

        sql = insertion_sql_head + " VALUES " + ",".join(values)
        sql = sql.replace("<st_id>",str(t_n % 10))
        while True:
            if event.is_set():
                break
            print("input")
            start = time.time()
          
            cur.execute(sql)
                  
            diff = time.time() - start
            results["insertions"].append( (start,batch_size) )     
            if diff < 1:
                time.sleep(1-diff)
            else:
                print(f"insertion of {batch_size} points took to long ({diff}s)")
    except Exception as e:
        results["status"] = "failed"
        print(e)
        message = str(e)
        if "table busy" in message:
                  print("questdb can not handle insertions from multiple threads")
        else:
                  print("insertion rate to high")

       

def delete_data(date= "2019-04-30T00:00:00", host = "localhost", dataset = "d1"):
    print("cleaning up questdb")
    conn = psycopg2.connect(user="admin",
          password="quest",
          host=host,
          port="8812",
          database="d1")
    start = time.time()
    cur = conn.cursor()
    sql = f"""create table table_copy as (select * from {dataset} where ts < '{date}') timestamp (ts) PARTITION BY DAY; """
    cur.execute(sql)
    cur.execute(f"drop table {dataset};")
    cur.execute(f"rename table table_copy to {dataset};")
