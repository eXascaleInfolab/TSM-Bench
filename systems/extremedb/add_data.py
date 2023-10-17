from threading import Thread
from threading import Event
import exdb
import time


def input_data(t_n,event, data , results , batch_size = 10, host = "localhost", dataset = "d1"):
    results["evaluated"] = True
    try:
        exdb.init_runtime(debug = True, shm = False, disk = False, tmgr = 'mursiw')
        conn = exdb.connect(host,5001)
        cur = conn.cursor()
        cur.execute("set append_mode true")
        data = data
        insertion_sql_head = "INSERT or UPDATE INTO "+dataset+" (id_station , " + ",".join(["s"+str(i) for i in range(100)]) + ")"
        values = [f"('{data['stations'][i]}' ,  {', '.join([str(s_n) for s_n in data['sensors'][i]])})" for i in range(batch_size)]
        sql = insertion_sql_head + " VALUES " + ",".join(values)
        sql = sql.replace("<st_id>",str(t_n%10))
        print(sql)
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
                print(f"insertion of {batch_size} points  took to long ({diff}s)")
    except Exception as e:
        results["status"] = "failed"
        print(e)
        print("extreme db execution failed")


def delete_data(date= "2019-04-1 00:00:00", host = "localhost", dataset = "d1"):
        import datetime
        exdb.init_runtime(debug = False, shm = False, disk = False, tmgr = 'mursiw')
        con = exdb.connect(host, 5001)
        curs = con.cursor()
        curs.execute(f"DROP table {dataset}")
        curs.execute(f"CREATE TABLE {dataset} (id_station string PRIMARY KEY, t sequence(TIMESTAMP asc), s0 sequence(DOUBLE), s1 sequence(DOUBLE), s2 sequence(DOUBLE), s3 sequence(DOUBLE), s4 sequence(DOUBLE), s5 sequence(DOUBLE), s6 sequence(DOUBLE), s7 sequence(DOUBLE), s8 sequence(DOUBLE), s9 sequence(DOUBLE), s10 sequence(DOUBLE), s11 sequence(DOUBLE), s12 sequence(DOUBLE), s13 sequence(DOUBLE), s14 sequence(DOUBLE), s15 sequence(DOUBLE), s16 sequence(DOUBLE), s17 sequence(DOUBLE), s18 sequence(DOUBLE), s19 sequence(DOUBLE), s20 sequence(DOUBLE), s21 sequence(DOUBLE), s22 sequence(DOUBLE), s23 sequence(DOUBLE), s24 sequence(DOUBLE), s25 sequence(DOUBLE), s26 sequence(DOUBLE), s27 sequence(DOUBLE), s28 sequence(DOUBLE), s29 sequence(DOUBLE), s30 sequence(DOUBLE), s31 sequence(DOUBLE), s32 sequence(DOUBLE), s33 sequence(DOUBLE), s34 sequence(DOUBLE), s35 sequence(DOUBLE), s36 sequence(DOUBLE), s37 sequence(DOUBLE), s38 sequence(DOUBLE), s39 sequence(DOUBLE), s40 sequence(DOUBLE), s41 sequence(DOUBLE), s42 sequence(DOUBLE), s43 sequence(DOUBLE), s44 sequence(DOUBLE), s45 sequence(DOUBLE), s46 sequence(DOUBLE), s47 sequence(DOUBLE), s48 sequence(DOUBLE), s49 sequence(DOUBLE), s50 sequence(DOUBLE), s51 sequence(DOUBLE), s52 sequence(DOUBLE), s53 sequence(DOUBLE), s54 sequence(DOUBLE), s55 sequence(DOUBLE), s56 sequence(DOUBLE), s57 sequence(DOUBLE), s58 sequence(DOUBLE), s59 sequence(DOUBLE), s60 sequence(DOUBLE), s61 sequence(DOUBLE), s62 sequence(DOUBLE), s63 sequence(DOUBLE), s64 sequence(DOUBLE), s65 sequence(DOUBLE), s66 sequence(DOUBLE), s67 sequence(DOUBLE), s68 sequence(DOUBLE), s69 sequence(DOUBLE), s70 sequence(DOUBLE), s71 sequence(DOUBLE), s72 sequence(DOUBLE), s73 sequence(DOUBLE), s74 sequence(DOUBLE), s75 sequence(DOUBLE), s76 sequence(DOUBLE), s77 sequence(DOUBLE), s78 sequence(DOUBLE), s79 sequence(DOUBLE), s80 sequence(DOUBLE), s81 sequence(DOUBLE), s82 sequence(DOUBLE), s83 sequence(DOUBLE), s84 sequence(DOUBLE), s85 sequence(DOUBLE), s86 sequence(DOUBLE), s87 sequence(DOUBLE), s88 sequence(DOUBLE), s89 sequence(DOUBLE), s90 sequence(DOUBLE), s91 sequence(DOUBLE), s92 sequence(DOUBLE), s93 sequence(DOUBLE), s94 sequence(DOUBLE), s95 sequence(DOUBLE), s96 sequence(DOUBLE), s97 sequence(DOUBLE), s98 sequence(DOUBLE), s99 sequence(DOUBLE));")
	# curs.execute("trace on")
        curs.execute(f"insert or update into {dataset} select id_station,(substr(t,1,10)||' '||substr(t,12,8))::timestamp::bigint,s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20,s21,s22,s23,s24,s25,s26,s27,s28,s29,s30,s31,s32,s33,s34,s35,s36,s37,s38,s39,s40,s41,s42,s43,s44,s45,s46,s47,s48,s49,s50,s51,s52,s53,s54,s55,s56,s57,s58,s59,s60,s61,s62,s63,s64,s65,s66,s67,s68,s69,s70,s71,s72,s73,s74,s75,s76,s77,s78,s79,s80,s81,s82,s83,s84,s85,s86,s87,s88,s89,s90,s91,s92,s93,s94,s95,s96,s97,s98,s99 from foreign table(path='../../../../../datasets/{dataset}.csv', skip=1) as {dataset}_h;")
