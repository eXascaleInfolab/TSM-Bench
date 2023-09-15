import os

curr_dir = os.getcwd()

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


from systems.clickhouse.start import launch
from systems.clickhouse.run_system import run_query
from systems.clickhouse.add_data import (input_data , delete_data)
os.chdir(curr_dir)
