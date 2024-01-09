import os
import sys
import importlib
import time

if os.path.basename(os.getcwd()) == "integration":
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.getcwd())

from utils.query_template_loader import load_query_templates
from utils.run_query import run_query
from systems.utils.connection_class import Connection

from pymongo import MongoClient


if __name__ == "__main__":
    #set workingdir 3 levels up


    from systems import clickhouse
    system = "mongodb"
    system_module =  importlib.import_module(f"systems.{system}")

    system_module.launch()
    n_st = 9
    n_s = 100
    dataset = "d1"
    date = "2019-04-29T23:59:50"
    rangeUnit = "day"
    rangeL = 1

    query_templates = load_query_templates(system)
    print("checking connection initialization\n")

    host = "localhost"
    mongo_uri = "mongodb://" + host + ":27017/"
    client = MongoClient(mongo_uri)
    print("server info", client.server_info())
    db = client["d1"]
    collection = db[dataset]
    test_result = collection.find().limit(10)
    print(test_result)
    time.sleep(3)
    for t in test_result:
        print(t)

    system_connection : Connection = system_module.get_connection(host="localhost", dataset=dataset)

    print("checking query parsing\n")
    for i , query_template in  enumerate(query_templates):
        query_template = query_template.replace("<db>", dataset)
        assert isinstance(query_template, str)

        print(" ######################### query" , i+1 , "#########################")
        print("base template:\n", query_template , "\n\n")
        parsed_query_template = system_module.parse_query(query_template, date=date , rangeL=rangeL , rangeUnit = rangeUnit ,
                                                          sensor_list= ("s1","s2","s3"),station_list=("st1", "st2"))
        print("parsed query template:\n" , parsed_query_template)



        query_results = system_connection.execute(parsed_query_template)

        print("query result:\n" )
        for result in query_results:
            print(result)

        print()

        # query_result = run_query(system_module, query_template, rangeL, rangeUnit, n_st, n_s, 4, dataset, host="localhost" , log=True)
        # print(query_result)
        # for document in query_result:
        #     print(document)
        time.sleep(3)