import psycopg2
import time

def input_data(t_n,event, data, results , batch_size, host="localhost", dataset = "d1"):
    try:
        CONNECTION = f"postgres://postgres:postgres@{host}:5432/postgres"
        conn = psycopg2.connect(CONNECTION)
        conn.autocommit = True
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
            if diff < 1:
                time.sleep(1-diff)
            else:
                print(f"insertion of {batch_size} points took to long ({diff}s)")
    except:
        results["status"] = "failed"


def delete_data(date= "2019-04-1 00:00:00", host = "localhost", dataset = "d1"):
    CONNECTION = f"postgres://postgres:postgres@{host}:5432/postgres"
    conn = psycopg2.connect(CONNECTION)
    conn.autocommit = True
    print("cleaning up the timescale database")
    start = time.time()
    sql = f"SELECT drop_chunks('{dataset}', newer_than => '{date}');"
    cur = conn.cursor()
    time.sleep(5)
    cur.execute(sql)
