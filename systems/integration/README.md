# System Integration

## Prerequisites
- The offline workload needs to be executed once
- The new system should:
    - provide a Python client library
    - support bulk loading using a CSV format
  

## Integration steps

- Create a folder with the name of your system under `systems/` and install your database inside.
- Install the Python client library inside the virtual environment (TSMvenv).
- Load the datasets located under the `datasets/` folder. The column names of the datasets are: `time`, `id_station`, and `s0,s1 ... s99`.
 Examples of loading scripts are provided in `systems/{system}/load.sh`. 
  

- Create a file called `queries.sql` that implements the queries. Make sure to keep the variables \<sid\> ,\<stid\> and \<timestamp\> as placeholders (see example [here](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/systems/monetdb/queries.sql)). Each query should be added as a new line.
- Create a script called `launch.sh` to launch the database (see example [here](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/systems/influx/launch.sh)).
- Create a Python script called  `run_system.py` to run the queries. The script should follow this [template](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/systems/run_system_template.py).
    - **Note**: The timestamp format should be updated according to one of the system (e.g., "YYYY-MM-DDTHH:mm:ss" for MonetDB, "YYYY-MM-DD HH:mm:ss" for QuestDB, etc.).
- Add the name of your system's folder to [config.py](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/systems/config.py).
- Execute the [offline worloakd](https://github.com/eXascaleInfolab/TSM-Bench/blob/main/README.md#experiments). The benchmark should report the runtime of the new system
- To execute the online workload,  three additional scripts need to be added:
    - `__init__.py`: script to use your folder as a Python module that should follow this [template](https://github.com/eXascaleInfolab/TSM-Bench/blob/main/systems/integration/__init__template.py). You need to replace "system" with "new\_system\_name".
    - `start.py`: script to launch your system that should follow this [template](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/systems/integration/start_template.py).
    - `add_data.py`: script to add and delete data that should follow this [template](https://github.com/eXascaleInfolab/TSM-Bench/blob/main/systems/integration/add_tempalte.py).


# Query Addition

To add additional queries to the benchmark, users can simply add the new queries under each system's `{system}/queries.sql` file. Queries order should be respected as queries are referred to by their order (e.g., q8 is the eighth query in the file).
