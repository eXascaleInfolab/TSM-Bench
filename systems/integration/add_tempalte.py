import time

### import the python client
#from clickhouse_driver import Client
#from clickhouse_driver import connect as connect_ClickHouse


def input_data(t_n, event, data , results,  batch_size = 1000, host = "localhost" , dataset = "d1"):
    """
    Params:
          t_n : thread number
          event: call back event to stop the thread
          data : data to ingest
          results : where to store the results
          batch_size : amount or rows inserted,
          host: connection to the database
          dataset: dataset to ingest
    """
  
    results["evaluated"] = True
    try:
        #### Connect to the database
        ###conn = connect_ClickHouse(f"clickhouse://{host}")
        ###cur = conn.cursor()

        ###create your insertion sql data contains keys "timesamps" : list , "stations" : list, and "sensors" : lists or lists 
        ##insertion_sql_head = "insert into "+dataset+" (time, id_station ," + ",".join(["s"+str(i) for i in range(100)]) + ")"
        ###values = [f"('{data['time_stamps'][i]}', '{data['stations'][i]}', {', '.join([str(s_n) for s_n in data['sensors'][i]])})" for i in range(batch_size)]
        ###sql = insertion_sql_head + " VALUES " + ",".join(values)
        ### sql = sql.replace("<st_id>",str(t_n % 10))
        while True:
            if event.is_set():
                break
            start = time.time()

            ### Execute the sql here
            ###cur.execute(sql)
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
    ### delete the data above the time stamp inside the database
    #conn = connect_ClickHouse(f"clickhouse://{host}")
    #print("cleaning up clickhouse database")
    #cur = conn.cursor()
    #time.sleep(4)
    #res = cur.execute(f"ALTER TABLE {dataset} DELETE where time > TIMESTAMP '{date}';")
