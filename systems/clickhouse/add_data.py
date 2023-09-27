import psycopg2
import time


from clickhouse_driver import Client
from clickhouse_driver import connect as connect_ClickHouse


def input_data(t_n, event, data , results,  batch_size = 1000, host = "localhost" , dataset = "d1"):
    results["evaluated"] = True
    try:
        conn = connect_ClickHouse(f"clickhouse://{host}")
        cur = conn.cursor()
        data = data
        insertion_sql_head = "insert into "+dataset+" (time, id_station ," + ",".join(["s"+str(i) for i in range(100)]) + ")"
        values = [f"('{data['time_stamps'][i]}', '{data['stations'][i]}', {', '.join([str(s_n) for s_n in data['sensors'][i]])})" for i in range(batch_size)]
        sql = insertion_sql_head + " VALUES " + ",".join(values)
        sql = sql.replace("<st_id>",str(t_n % 10))
        while True:
            if event.is_set():
                break
            start = time.time()
            cur.execute(sql)
            diff = time.time() - start
            results["insertions"].append( (start,batch_size) )   
            if diff <= 1:
                time.sleep(1-diff)
            else:
                print(f"insertion to slow took {diff}s")
             
    except Exception as e:
        results["status"] = "failed"
        raise e
              


def delete_data(date= "2019-04-30T00:00:00",host="localhost" , dataset = "d1"):
    conn = connect_ClickHouse(f"clickhouse://{host}")
    print("cleaning up clickhouse database")
    cur = conn.cursor()
    time.sleep(4)
    res = cur.execute(f"ALTER TABLE {dataset} DELETE where time > TIMESTAMP '{date}';")
    time.sleep(10)
    print(res)