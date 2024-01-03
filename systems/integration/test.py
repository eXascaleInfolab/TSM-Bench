import os
import sys
import importlib




if __name__ == "__main__":
    #set workingdir 3 levels up
    if os.path.basename(os.getcwd()) == "integration":
        os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    sys.path.append(os.getcwd())

    from systems import clickhouse
    system = "clickhouse"
    system_module =  importlib.import_module(f"systems.{system}")

    system_module.launch()
    n_st = 3
    n_s = 2
    dataset = "d1"

    query_templates = system_module.load_query_templates(system)
    print(query_templates)
    for i , query_template in  enumerate(query_templates):
        print("base tamplete", query_template)
        print("parsed query template" , system_module.parse_query_template(query_template, n_st, n_s,dataset=dataset))


