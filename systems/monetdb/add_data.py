
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


def input_data(t_n,event,data,results, batch_size, host="localhost", dataset = "d1"):    
    results["evaluated"] = True
    try:
        global conn
        if conn is None:
            conn = pymonetdb.connect(username="monetdb", port=54320, password="monetdb", hostname=host, database="mydb", autocommit = True)
        cur = conn.cursor()
        isolation_level = "SERIALIZABLE" # "REPEATABLE READ" #"READ COMMITTED"
        cur.execute(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}")

        data = data
        insertion_sql_head = "insert into "+dataset+" (time, id_station ," + ",".join(["s"+str(i) for i in range(100)]) + ")"
        values = [f"('{data['time_stamps'][i]}', '{data['stations'][i]}', {', '.join([str(s_n) for s_n in data['sensors'][i]])})" for i in range(batch_size)]
        print("time stamps", data['time_stamps'][batch_size-10:batch_size])
        sql = insertion_sql_head + " VALUES " + ",".join(values)
        sql = sql.replace("<st_id>",str(t_n))
        # print("sql",sql)
        while True:
            print("input")
            if event.is_set():
                if conn is not None: 
                    conn.close()
                    conn = None
                break

            start = time.time()
            
            cur.execute(sql)

            diff = time.time() - start
                  
            results["insertions"].append( (start,batch_size) )   
            if diff <= 1:
                time.sleep(1-diff)
            else:
                print(f"insertion to slow (took {diff}s)")

    except Exception as e:
        import traceback
        results["status"] = "failed"
        print(traceback.format_exc())
        print(e)
    return 





def delete_data(date= "2019-04-1 00:00:00", host = "localhost", dataset = "d1"):
    conn = pymonetdb.connect(username="monetdb", port=54320, password="monetdb", hostname=host, database="mydb", autocommit = True)
    print("cleaning up monetdb database")
    cur = conn.cursor()
    time.sleep(10) # concurrency safety
    res = cur.execute(f"DELETE from {dataset} where time > TIMESTAMP '{date}';")
