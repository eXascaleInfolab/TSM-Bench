import psycopg2
import time



def input_data(event, data , batch_size = 1000, host = "localhost"):
        conn = psycopg2.connect(user="admin",
          password="quest",
          host=host,
          port="8812",
          database="d1")
        cur = conn.cursor()
        data = data
        insertion_sql_head = "insert into d1 (ts, id_station ," + ",".join(["s"+str(i) for i in range(100)]) + ")"
        values = [f"('{data['time_stamps'][i]}', '{data['stations'][i]}', {', '.join([str(s_n) for s_n in data['sensors'][i]])})" for i in range(batch_size)]

        sql = insertion_sql_head + " VALUES " + ",".join(values)
        #print(sql)
        while True:
            if event.is_set():
                break
                  
            start = time.time()
          
            cur.execute(sql)
                  
            diff = time.time() - start
            print(f"inserted {batch_size} in {diff}s")
            if diff < 1:
                time.sleep(1-diff)


def delete_data(date= "2019-04-30T00:00:00", host = "localhost"):
    conn = psycopg2.connect(user="admin",
          password="quest",
          host=host,
          port="8812",
          database="d1")
    start = time.time()
    cur = conn.cursor()
    sql = f"""create table table_copy as (select * from d1 where ts < '{date}') timestamp (ts) PARTITION BY DAY; """
    cur.execute(sql)
    cur.execute("drop table d1;")
    cur.execute("rename table table_copy to d1;")
