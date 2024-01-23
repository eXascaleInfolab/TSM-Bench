import os

curr_dir = os.getcwd()

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


from systems.timescaledb.run_system import run_query , launch , stop , get_connection , parse_query
from systems.timescaledb.add_data import delete_data , generate_insertion_query
os.chdir(curr_dir)

