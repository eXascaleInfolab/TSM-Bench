import os
import sys
import importlib

if os.path.basename(os.getcwd()) == "integration":
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.getcwd())

from utils.query_template_loader import load_query_templates
from utils.run_query import run_query

if __name__ == "__main__":
    #set workingdir 3 levels up


    from systems import clickhouse
    system = "mongodb"
    system_module =  importlib.import_module(f"systems.{system}")

    system_module.launch()
    n_st = 3
    n_s = 2
    dataset = "d1"
    date = "2019-03-01T00:17:40"
    rangeUnit = "day"
    rangeL = 1

    query_templates = load_query_templates(system)
    print(query_templates)
    for i , query_template in  enumerate(query_templates):
        query_template = query_template.replace("<db>", dataset)
        print(" ######################### query" , i+1 , "#########################")
        print("base tamplete:\n", query_template , "\n\n\n")
        parsed_query_template = system_module.parse_query(query_template, date=date , rangeL=rangeL , rangeUnit = rangeUnit ,
                                                          sensor_list= ("s1","s2","s3"),station_list=("st1", "st2"))
        print("parsed query template:\n" , parsed_query_template)

        #run_query(system_module, parsed_query_template, rangeL, rangeUnit, n_st, n_s, 4, dataset, host="localhost")
        # system_module.run_query(parsed_query_template, n_st=n_st, n_s=n_s , n_it = 3 , dataset=dataset , rangeL=rangeL , rangeUnit = rangeUnit)

