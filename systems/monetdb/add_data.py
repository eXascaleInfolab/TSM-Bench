
import pymonetdb
import time

def input_data(event,data,batch_size, host="localhost"):
    conn = pymonetdb.connect(username="monetdb", port=54320, password="monetdb", hostname=host, database="mydb", autocommit = True)
    cur = conn.cursor()
    data = data
        
    insertion_sql_head = "insert into d1 (time, id_station ," + ",".join(["s"+str(i) for i in range(100)]) + ")"
    values = [f"('{data['time_stamps'][i]}', '{data['stations'][i]}', {', '.join([str(s_n) for s_n in data['sensors'][i]])})" for i in range(batch_size)]
    sql = insertion_sql_head + " VALUES " + ",".join(values)
    while True:
        if event.is_set():
            conn.close()
            break
                  
        start = time.time()
          
        cur.execute(sql)
                  
        diff = time.time() - start
        if diff < 1:
            time.sleep(1-diff)
        else:
            print(f"insertion of {batch_size} points took to long ({round(diff,3)}s)")
    return 





def delete_data(date= "2019-04-1 00:00:00", host = "localhost"):
    conn = pymonetdb.connect(username="monetdb", port=54320, password="monetdb", hostname=host, database="mydb", autocommit = True)
    print("cleaning up monetdb database")
    cur = conn.cursor()
    time.sleep(10) # concurrency safety
    res = cur.execute(f"DELETE from d1 where time > TIMESTAMP '{date}';")