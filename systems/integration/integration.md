# System Integration

## Prerequisites
- Ubuntu 20
- The system needs to provide a Python connection
- The system needs to support csv format for data loading

## Intergration steps

 - Create a folder with the name of your system under `/systems` and install your database inside.
 - Install the Python client library inside the virtual environment (TSMvenv).
 - Load the datasets
   -  the column names from the datasets are: time , id_station and s0 ,s1 .. s99
   -  The relative location of the dataset is  ../../datasets/dataset.csv

   Take a look at the Examples: [ ExtremeDB load.sh](https://github.com/eXascaleInfolab/TSM-Bench/blob/tree/main/systems/monetdb/load.sh) or [MonetDB load.sh](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/systems/extremedb/load.sh) 

- Create a file called `queries.sql`that implements the queries. Make sure to keep the variables \<sid\> ,\<stid\> and \<timestamp\> as placeholders (see example [here](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/systems/monetdb/queries.sql)).
- Create a file called `launch.sh` to launch the database (see example [here](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/systems/influx/launch.sh)).
- Create a python script called  `run_system.py`to run the queries. The script should adhere to this [template](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/systems/run_system_template.py).
- Add the name of your system's folder to [config.py](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/systems/config.py).

- To use the online workload add the additional files:
    - `__init__.py`: s script to use your folder as a Python module. The script should follow this [template](https://github.com/eXascaleInfolab/TSM-Bench/blob/main/systems/integration/__init__template.py) and replacing "system" with "your\_system\_name".
    - `start.py`: a script to launch your system. The script should follow this [template](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/systems/integration/start_template.py).
    - `add_data.py`: a script to add and delete data.  The script should follow this [template](https://github.com/eXascaleInfolab/TSM-Bench/blob/main/systems/integration/add_tempalte.py).


