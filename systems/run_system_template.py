from datetime import datetime
from tqdm import tqdm
import argparse
import os
import time
import statistics as stats
import numpy as np
import random
import sys
import pandas as pd
import json

# setting path
sys.path.append('../')
from library import *

### TODO: import your python client library
### import pymonetdb

# Generate Random Values
random.seed(1)
set_st = [str(random.randint(0,9)) for i in range(500)]
set_s = [str(random.randint(0,99)) for i in range(500)]
set_date = [random.random() for i in range(500)]


def run_query(query, rangeL , rangeUnit, n_st , n_s , n_it,host="localhost"):
    
    ### OPTIONAL convert invalid range units
    #if rangeUnit in ["week","w","WEEK"]:
    #    rangeUnit = "day"
    #    rangeL = rangeL*7
    
    ### TODO: connect to the system your system
    # eg
    #conn = pymonetdb.connect(username="monetdb", port=54320, password="monetdb", hostname=host, database="mydb")
    #cursor = conn.cursor()
    
    runtimes = []
    full_time = time.time()
    for it in tqdm(range(n_it)):
        date = random_date("2019-04-01T00:00:00", "2019-04-30T00:00:00", set_date[(int(rangeL)*it)%500], dform = '%Y-%m-%dT%H:%M:%S')
        
        #start building the queriy by replacing the place holder values
        temp = query.replace("<timestamp>", date)
        temp = temp.replace("<range>", str(rangeL))
        temp = temp.replace("<rangesUnit>", rangeUnit)
        
        
        # stations
        li = ['st' + str(z) for z in random.sample(range(10), n_st)]
        q = "(" + "'" + li[0] + "'"
        for j in li[1:]:
            q += ', ' + "'" + j + "'"
        q += ")"
    
        temp = temp.replace("<stid>", q)
        temp = temp.replace("<stid1>", f"{random.randint(1,10)}")
        temp = temp.replace("<stid2>", f"{random.randint(1,10)}") 
    
        # sensors
        li = ['s' + str(z) for z in random.sample(range(100), n_s)]
        q = li[0]
        q_filter = '(' + li[0] + ' > 0.95' 
        q_avg = 'avg(' + li[0] + ')'
        for j in li[1:]:
            q += ', ' + j
            # q_filter += ' OR ' + j + ' > 0.95'
            q_avg += ', ' + 'avg(' + j + ')'
        
        ### replace place holders in your queries
        temp = temp.replace("<sid>", q)
        temp = temp.replace("<sid1>", str(set_s[(rangeL*it)%500]))
        temp = temp.replace("<sid2>", str(set_s[(rangeL*(it+1))%500]))
        temp = temp.replace("<sid3>", str(set_s[(rangeL*(it+2))%500]))
        temp = temp.replace("<sfilter>", q_filter + ')')
        temp = temp.replace("<avg_s>", q_avg)
        


        # OPTIONAL
        # if your system does not suport a=(b,c,d) map it to ors
        #match a=(b,c,...) make it a=b or a=c or ...
        #
        #import re 
        #
        #equality_missmatches = re.findall(r"\b\w+\s*=\s*\([^)]*?,[^)]*?\)",temp)
        #for equality_missmatch in  equality_missmatches:
        #    pattern , options = equality_missmatch.split("=")
        #    options = options.replace(")","").replace("(","").split(",")    
        #    res = "(" +  " or ".join( [ pattern+"= "+o  for o in options ]) +  ")"   
        #    temp = temp.replace(equality_missmatch,res)

        start = time.time()
        ### TODO execute the query
        #e.g cursor.execute(temp) or client.query(temp)
        #results_ = cursor.fetchall()

        diff = (time.time()-start)*1000
        runtimes.append(diff)
        if time.time() - full_time > 200 and it > 5: 
            break  
            
    ### TODO: close your connection
    ##conn.close()
    return stats.mean(runtimes), stats.stdev(runtimes)




if __name__ == "__main__":
    print('launching system')

    import os
    import subprocess
    from subprocess import Popen, PIPE, STDOUT, DEVNULL # py3k
    
    ## OPTIONAL set needed envioerment variables here
    ## os.environ.update({ "name" : "value" , ...)
    
    # launch the system 
    process = Popen(['sh', 'launch.sh', '&'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    # TODO: remove this line if you should not wait for sh.launch to terminate (i.e the process needs to be running in the background) if
    stdout, stderr = process.communicate() 
    
    ## if you removed the previous line adjust the sleep command to ensure your system has started up
    process = Popen(['sleep', '2'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    stdout, stderr = process.communicate() 
    
    args = parser.parse_args()
       
    def query_f(query, rangeL = args.range, rangeUnit = args.rangeUnit, n_st = args.def_st, n_s = args.def_s, n_it = args.n_it):
        return run_query(query, rangeL=rangeL, rangeUnit = rangeUnit ,n_st = n_st , n_s = n_s , n_it = n_it)

    run_system(args,"extremedb",query_f)

    # Stop the system
    process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    stdout, stderr = process.communicate()

