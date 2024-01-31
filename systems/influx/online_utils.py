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

def delete_data(date= "2019-04-1T00:00:00", host = "localhost", dataset = "d1"):
    print("celaning up influx")
    start = time.time()
    client = InfluxDBClient(host=host, port=8086, username='user', database=dataset)
    
    result = client.query(f"""DELETE FROM "sensor" where time > '{date}Z' """)
    client.close()
    print(result)
    client.close()
    time.sleep(5)
