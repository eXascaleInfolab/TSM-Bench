# Benchmark

___
## Prerequisites and dependencies

- Ubuntu 18 or higher
- Clone this repository
- All other dependencies will be installed via the install script.

___
## Build

- Install all dependencies (~ 3 mins)

```bash
cd Databases
sh install_dependencies.sh
```

- Build dataset D1 (~ 11 mins)

```bash
cd ../Datasets/
sh install.sh
```


- Download and install all systems

```bash
cd Databases
sh install_all.sh
```

To build a particular database, run the installation script located in the database folder. For example, to install influxdb

```bash
cd Databases/influx
sh install.sh
```



___
## Running eval

Each of the databases has a dedicated subfolder under `Databases` folder, in which there is a dedicated directory for each experiment. In order to run an experiment, go to the directory of the experiment and use the Python3 script there. For example,

