import os

curr_dir = os.getcwd()

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


from systems.extremedb.run_system import run_query , launch , stop ,get_connection
from systems.extremedb.add_data import (input_data , delete_data)
os.chdir(curr_dir)
