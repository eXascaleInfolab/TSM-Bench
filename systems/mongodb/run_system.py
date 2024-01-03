"""
Example of integrating a system into TSM-Bench using mongodb
"""

# requiered python libary for mongdb
from pymongo import MongoClient

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
    else:
        raise Exception("rangeUnit not supported")
    return date.strftime('%Y-%m-%dT%H:%M:%S')


def parse_query(query, date, rangeL, rangeUnit, sensor_list, station_list):
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


    mongodb has no time itnerval notation so we add a second time stamp
    <from_time> = date - rangeL*rangeUnit
    additionaly we add a filter for the sensors projection:
    <sid_proj> : sensor ids for projection
    """

    # replace <stid> with [ commaserperated station ids]
    stations = "[" + ",".join(station_list) + "]"
    query = query.replace("<stid>", stations)

    # replace sensor list with [ commaserperated sensor ids]
    sensors = "[" + ",".join(sensor_list) + "]"
    query = query.replace("<sid>", sensors)

    # replace <timestamp> with the query
    query = query.replace("<timestamp>", date)

    # compute the from_time and replace <from_time>
    from_time = decrease_date(date, rangeL, rangeUnit)
    query = query.replace("<from_time>", from_time)

    ## add the sensor projection filte
    sensor_proj = ",".join([f"'{s}' : 1" for s in sensor_list])
    query = query.replace("<sid_proj>", sensor_proj)

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
    db = client["db"]
    collection = db[dataset]

    def conn_close_f():
        client.close()

    def execute_query_f(query):
        """ queries as parsed by parse_query """
        cursor = collection.find(query)
        return cursor.fetchall()

    def insert_f(data):
        """ sting  parsed by generate_insertion_query  """
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

