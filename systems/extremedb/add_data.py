from threading import Thread
from threading import Event
import exdb
import time


def input_data(event, data , batch_size = 1000, host = "localhost"):
    from systems.online_library import generate_continuing_data
    exdb.init_runtime(debug = True, shm = False, disk = False, tmgr = 'mursiw')
    conn = exdb.connect(host,5001)
    cur = conn.cursor()
    cur.execute("set append_mode true")
    data = data
    print(cur.execute("select count(*) from d1"))
    insertion_sql_head = "INSERT or UPDATE INTO d1 (id_station ," + ",".join(["s"+str(i) for i in range(100)]) + ")"
    values = [f"('{data['stations'][i]}', {', '.join([str(s_n) for s_n in data['sensors'][i]])})" for i in range(batch_size)]
    sql = insertion_sql_head + " VALUES " + ",".join(values)
    print("query created")

    while True:
        if event.is_set():
            break
                  
        start = time.time()
          
        cur.execute(sql)
                  
        diff = time.time() - start
        print(f"inserted {batch_size} in {diff}s")
        if diff < 1:
            time.sleep(1-diff)
        else:
            print(f"insertion of {batch_size} points  took to long ({diff}s)")




def delete_data(date= "2019-04-1 00:00:00", host = "localhost"):
    conn = exdb.connect(host,5001)
    print("cleaning up extremedb system")
    cur = conn.cursor()
    sql = "delete from d1 where time > date"
    cur.execute(sql)

          