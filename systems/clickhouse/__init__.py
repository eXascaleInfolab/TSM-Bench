import os

curr_dir = os.getcwd()

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
    
from systems.clickhouse.run_system import *
from systems.clickhouse.online_utils import input_data , delete_data , generate_insertion_query

os.chdir(curr_dir)
