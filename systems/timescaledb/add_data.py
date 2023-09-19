import psycopg2
import time

def input_data(event, data, results , batch_size, host="localhost"):
    try:
        from systems.online_library import generate_continuing_data
        CONNECTION = f"postgres://postgres:postgres@{host}:5431/postgres"
        conn = psycopg2.connect(CONNECTION)
        conn.autocommit = True
        cur = conn.cursor()
        data = data
        insertion_sql_head = "insert into d1 (time, id_station ," + ",".join(["s"+str(i) for i in range(100)]) + ")"
        values = [f"('{data['time_stamps'][i]}', '{data['stations'][i]}', {', '.join([str(s_n) for s_n in data['sensors'][i]])})" for i in range(batch_size)]
        sql = insertion_sql_head + " VALUES " + ",".join(values)
        while True:
            if event.is_set():
                break
                  
            start = time.time()
                  
            cur.execute(sql)
                  
            diff = time.time() - start
            results["insertions"].append( (start,batch_size) )     
            if diff < 1:
                time.sleep(1-diff)
            else:
                print(f"insertion of {batch_size} points took to long ({diff}s)")
    except:
        results["status"] = "failed"


def delete_data(date= "2019-04-1 00:00:00", host = "localhost"):
    CONNECTION = f"postgres://postgres:postgres@{host}:5431/postgres"
    conn = psycopg2.connect(CONNECTION)
    conn.autocommit = True
    print("cleaning up the timescale database")
    start = time.time()
    sql = f"SELECT drop_chunks('d1', newer_than => '{date}');"
    cur = conn.cursor()
    time.sleep(5)
    cur.execute(sql)
