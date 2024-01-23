"""
Example of integrating a system into TSM-Bench using mongodb
"""
from datetime import datetime, timedelta

# requiered python libary for mongdb
from pymongo import MongoClient
import json
from systems.utils import connection_class, change_directory


def decrease_date(date, rangeL, rangeUnit):
    """
    mongodb does not support the notation - time interval so we need to compute the second date seperatly

    :param date: date in the format of YYYY-MM-DDTHH:mm:ssZ , i.e for mongodb we need to add Z at the end
    :param rangeL: e.g 1
    :param rangeUnit: e.g Day
    :return: date + rangeL*rangeUnit
    """

    from datetime import datetime, timedelta

    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')

    rangeUnit = rangeUnit.lower()

    if rangeUnit == "minute":
        date -= timedelta(minutes=rangeL)
    elif rangeUnit == "hour":
        date -= timedelta(hours=rangeL)
    elif rangeUnit == "day":
        date -= timedelta(days=rangeL)
    elif rangeUnit == "week":
        date -= timedelta(weeks=rangeL)
    elif rangeUnit == "month":
        date -= timedelta(weeks=rangeL * 4)
    else:
        raise Exception("rangeUnit not supported")
    return date.strftime('%Y-%m-%dT%H:%M:%S')


def parse_query(query, date, rangeL, rangeUnit, sensor_list, station_list) -> str:
    """
    :param query: query_template (look below)
    :param date: 2019-03-01T00:17:40
    :param rangeL: e.g. 1
    :param rangeUnit: e.g. Day
    :param sensor_list: e.g. (s1,s2,s3)
    :param station_list: e.g. (st1,st2)
    :return: parsed query


    Query tempaltes may the following placeholders:
    <db> : database name
    <timestamp> : timestamp
    <range> : range length
    <rangesUnit> : range unit
    <sid> : sensor ids for 'in clause'
    <stid> : station ids for 'in clause'
    <sid1> : sensor id 1
    <sid2> : sensor id 2
    <sid3> : sensor id 3


    mongodb has no time interval notation so we add a second time stamp
    <from_time> = date - rangeL*rangeUnit
    additionaly we add a filter for the sensors projection:
    <sid_proj> : sensor ids for projection
    """

    # replace <stid> with [ commaserperated station ids]
    stations =   "[" + ",".join([f'"{station_id}"' for station_id in station_list]) + "]"
    query = query.replace("<stid>", stations)

    # replace sensor list with [ commaserperated sensor ids]
    sensors = "[" + ",".join(sensor_list) + "]"
    query = query.replace("<sid>", sensors)

    # replace <timestamp> with the query
    query = query.replace("<timestamp>", date)

    # compute the from_time and replace <from_time>
    from_time = decrease_date(date, rangeL, rangeUnit)
    query = query.replace("<timestamp_from>", from_time)

    ## add the sensor projection filter
    sensor_proj = ",".join([f"'{s}' : 1" for s in sensor_list])
    query = query.replace("<sid_proj>", sensor_proj)

    query = query.replace("<sid1>", "s1")
    query = query.replace(">sid2>", "s2")

    # insert the average over each sensor (Q3)
    # <avg_sid> ->  "avg_s_i": {"$avg": "$s_i"} , ... , "avg_s_n": {"$avg": "$s_n"}
    avg_sid = ','.join([f'"avg_{s_id}": {{ "$avg": "${s_id}" }} ' for s_id in sensor_list])
    query = query.replace("<avg_sid>" , avg_sid )

    # convert query to json and return it as a string
    # query = '{"id_station": {"$in": ["st1","st2"]}, "time": {"$gt": "2019-02-28T00:17:40", "$lt": "2019-03-01T00:17:40"}, "s1": {"$gt": 0.95}}'
    print(query)
    query = json.loads(query)
    query = json.dumps(query)
    print(query)
    return query





def get_connection(host="localhost", dataset=None, **kwargs):
    """
    :param host: host name
    :param dataset: dataset name
    :return: connection object for mongodb (see systems/utils/connection_class.py) to have a common interface.
    """
    # database is db
    mongo_uri = "mongodb://" + host + ":27017/"
    client = MongoClient(mongo_uri)
    db = client["d1"]
    collection = db[dataset]

    def conn_close_f():
        client.close()

    def execute_query_f(query):
        """ queries as parsed by parse_query
            A sepial case where query is not an sql query but a json string with outer keys find or aggregate
        """
        print("running mongodb query")

        def custom_decoder(dct):
            for key, value in dct.items():
                if isinstance(value, str):
                    try:
                        # Try to parse the string as a datetime
                        dct[key] = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
                    except ValueError:
                        # If it's not a valid datetime string, leave it as is
                        pass
            return dct

        query_dict = json.loads(query, object_hook=custom_decoder )


        # def insert_date_time_obj(json_query : dict):
        #     if 'time' in json_query:
        #         json_query["time"]["$gt"] = datetime.strptime(json_query["time"]["$gt"],'%Y-%m-%dT%H:%M:%S')
        #         json_query["time"]["$lt"] = datetime.strptime(json_query["time"]["$lt"],'%Y-%m-%dT%H:%M:%S')
        #     return json_query



        assert "find" in query_dict or "aggregate" in query_dict , f"for mongodb you need to specify the function to call: find or aggregate"
        if "find" in query_dict:
            print("find")
            json_query = query_dict["find"]
            print(json_query)

            result = collection.find(json_query)
        elif "aggregate" in query_dict:
            print("aggregate")
            json_query = query_dict["aggregate"]
            print(json_query)
            result = collection.aggregate(json_query)

        return result

    def insert_f(data):
        """ string value parsed by generate_insertion_query  """
        collection.insert_many(data)

    return connection_class.Connection(conn_close_f, execute_query_f, insert_f)


def launch():
    """
    launch your database system
    we suggest to use the change_directory context manager to make sure that you are in the correct directory
    and leave it once mongodb is launched
    """
    print('launching mongodb')
    from subprocess import Popen, PIPE, STDOUT, DEVNULL  # py3k

    with change_directory(__file__):
        process = Popen(['sh', 'launch.sh', '&'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

        process = Popen(['sleep', '2'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()


def stop():
    """
    stop your database system
    we suggest to use the change_directory context manager to make sure that you are in the correct directory
    and leave it once mongodb is stopped
    """
    print('stopping mongodb')
    from subprocess import Popen, PIPE, STDOUT, DEVNULL  # py3k

    with change_directory(__file__):
        process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()


#### Online compuation of the query ####

def generate_insertion_query(time_stamps: list, station_ids: list, sensors_values, dataset):
    """ generates the insertion query for mongodb passed to the write_f define in the connection
     https://www.mongodb.com/docs/manual/reference/method/db.collection.insertMany/  """

    insertion_dcouments = [
        "{ time:" + time + "id_station" + st_id + ", " + ", ".join(["s_id : " + s_v for s_v in sensor_values]) + '}'
        for time, st_id, sensor_values in zip(time_stamps, station_ids, sensors_values)]

    insertion_dcouments = str(insertion_dcouments).replace("'", '"')
    return insertion_dcouments


def delete_data(date="2019-04-30T00:00:00", host="localhost", dataset="d1"):
    """ cleans up the database by deleting all time points above a certain date

    https://docs.mongodb.com/manual/reference/method/db.collection.deleteMany/
    :param date: date in the format of YYYY-MM-DDTHH:mm:ss
    :param host: host name
    :param dataset: dataset name
    """

    mongo_uri = "mongodb://" + host + ":27017/"
    client = MongoClient(mongo_uri)
    db = client["db"]
    collection = db[dataset]
    collection.deleteMany({"time": {"$gt": date}})
    client.close()
