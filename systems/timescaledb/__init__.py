import os

curr_dir = os.getcwd()

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


from systems.timescaledb.start import launch
from systems.timescaledb.run_system import run_query
from systems.timescaledb.add_data import (input_data , delete_data)
os.chdir(curr_dir)
