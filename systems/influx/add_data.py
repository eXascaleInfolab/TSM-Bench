import time
from influxdb import InfluxDBClient

def generate_insertion_query(time_stamps: list, station_ids: list, sensors_values, dataset):
    #generates string with influx query seperated by ;
    # convert time stmap to influx format
    print(time_stamps)
    time_stamps = [str(int(time.mktime(time.strptime(t, "%Y-%m-%dT%H:%M:%S")) * 1000)) for t in time_stamps]
    print(time_stamps)

    result = ""
    for t,station, sensor_values in zip(time_stamps, station_ids, sensors_values):
        result += f"sensor,id_station={station} "
        result += ",".join([f"s{i}={v}" for i, v in enumerate(sensor_values)])
        result += f" {t};"
    result = result[:-1] # remove last ;
    return result

def input_data(t_n,event, data , results , batch_size = 1000, host = "localhost", dataset = "d1"):
        results["evaluated"] = True
        try:
            client = InfluxDBClient(host, port=8086, username='user')
            f = "sensor,id_station=st99 s0=<>,s1=0.256154,s2=0.353368,s3=0.264800,s4=0.340716,s5=0.888801,s6=0.098555,s7=0.990292,s8=0.006500,s9=0.197772,s10=0.056110,s11=0.711823,s12=0.113245,s13=0.203696,s14=0.749044,s15=0.637718,s16=0.197120,s17=0.396791,s18=0.868563,s19=0.503080,s20=0.403444,s21=0.050145,s22=0.434476,s23=0.649876,s24=0.001515,s25=0.970305,s26=0.473175,s27=0.563040,s28=0.310380,s29=0.273118,s30=0.551110,s31=0.308798,s32=0.783165,s33=0.950974,s34=0.926163,s35=0.802391,s36=0.226309,s37=0.432790,s38=0.114836,s39=0.347638,s40=0.432519,s41=0.838368,s42=0.638415,s43=0.944477,s44=0.735955,s45=0.419511,s46=0.152170,s47=0.333158,s48=0.566972,s49=0.028693,s50=0.491042,s51=0.604122,s52=0.764282,s53=0.577141,s54=0.267561,s55=0.432286,s56=0.157174,s57=0.851707,s58=0.213233,s59=0.095803,s60=0.982957,s61=0.841460,s62=0.533001,s63=0.090531,s64=0.386728,s65=0.363502,s66=0.281768,s67=0.431700,s68=0.852836,s69=0.398835,s70=0.760999,s71=0.160066,s72=0.475869,s73=0.028385,s74=0.111324,s75=0.948984,s76=0.575755,s77=0.741031,s78=0.625195,s79=0.057176,s80=0.590370,s81=0.498445,s82=0.879716,s83=0.717900,s84=0.597301,s85=0.596217,s86=0.407540,s87=0.750143,s88=0.736843,s89=0.264539,s90=0.457388,s91=0.054152,s92=0.486477,s93=0.525835,s94=0.204051,s95=0.694023,s96=0.558147,s97=0.668027,s98=0.166661,s99=0.745691" # 1556582400000"


            while True:
                if event.is_set():
                    client.close()
                    break

                start = time.time()
                
                write = client.write_points([f.replace("<>",str(t_n)) + " " + str(1556582400000+i*20000000) for i in range(batch_size)] , database= dataset , time_precision='ms', batch_size=batch_size ,protocol="line")
                diff = time.time() - start
                results["insertions"].append( (start,batch_size) )     
                if diff < 1:
                    time.sleep(1-diff)
                else:
                    print(f"insertion of {batch_size} points took to long ({round(diff,3)}s)")
        
        except Exception as e:
            print(e)
            print("influx failed to ingest data")
            results["status"] = "failed"
            


def delete_data(date= "2019-04-1T00:00:00", host = "localhost", dataset = "d1"):
    print("celaning up influx")
    start = time.time()
    client = InfluxDBClient(host=host, port=8086, username='user', database=dataset)
    
    result = client.query(f"""DELETE FROM "sensor" where time > '{date}Z' """)
    client.close()
    time.sleep(5)
