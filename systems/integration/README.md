# System Integration

## Prerequisites
- The benchmark needs to be ran once
- The system needs to provide a Python connection
- The system needs to support csv format for data loading
  

## Integration steps

- Create a folder with the name of your system under `systems/` and install your database inside.
- Install the Python client library inside the virtual environment (TSMvenv).
- Load the datasets located under the `datasets/` folder. The column names of the datasets are: time, id_station and `s0 ,s1 ... s99`
 Examples of loading are provided in `systems/{system}/load.sh`. 
  

- Create a file called `queries.sql`that implements the queries. Make sure to keep the variables \<sid\> ,\<stid\> and \<timestamp\> as placeholders (see example [here](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/systems/monetdb/queries.sql)).
- Create a script called `launch.sh` to launch the database (see example [here](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/systems/influx/launch.sh)).
- Create a python script called  `run_system.py`to run the queries. The script should follow this [template](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/systems/run_system_template.py).
- Add the name of your system's folder to [config.py](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/systems/config.py).
- You can now execute the offline queries and the benchmark should report the runtime of the new system and the existing ones
- To use the online workload add the additional files:
    - `__init__.py`: script to use your folder as a Python module. The script should follow this [template](https://github.com/eXascaleInfolab/TSM-Bench/blob/main/systems/integration/__init__template.py) and replacing "system" with "your\_system\_name".
    - `start.py`: script to launch your system. The script should follow this [template](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/systems/integration/start_template.py).
    - `add_data.py`: script to add and delete data.  The script should follow this [template](https://github.com/eXascaleInfolab/TSM-Bench/blob/main/systems/integration/add_tempalte.py).


