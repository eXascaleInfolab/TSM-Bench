# Benchmark

___
## Prerequisites and dependencies

- Ubuntu 18 or higher
- Clone this repository
- All other dependencies will be installed via the install script.

___
## Build

- Build all databases using the installation script located in the root folder

```bash
cd Databases
sh install_all.sh
```

To build a particular database, run the installation script located in the database folder. For example, to install influxdb

```bash
cd Databases/influx
sh install.sh
```

- Load all datasets

```bash
cd ../Datasets/
sh install.sh
```
___
## Datasets

___
## Execution Configuration

## Run all systems on a query

___
## Reproducibility of experiments


___
## Running eval

Each of the databases has a dedicated subfolder under `Databases` folder, in which there is a dedicated directory for each experiment. In order to run an experiment, go to the directory of the experiment and use the Python3 script there. For example,

