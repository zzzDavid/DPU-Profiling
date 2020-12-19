# DPU Latency and Power Profiling Tool

## Introduction

This repository contains a set of tools to deploy and test compiled model on Xilinx DPU.

- `utils/build/latency`: the binary executable to test latency
- `to_so.py`: converts all `*.elf` in `./elf` to `.so` files, and save them in `./so`
- `power.py`: runs all models presented in the `./so` folder, and save latency result in `./latency` directory. At finish, it writes out `test_time_stamps.txt`, the time stamps recording starting and finishing time of each model, used for segmenting power data which is recorded by another PC connected to the board.
- `latency.py`: runs all models presented in the `./so` folder, and save latency result in `./latency` directory.
- `divide_data.py`: segments `datalog.csv` according to `test_time_stamps.txt`, the results are saved at `./results_csv`
- `plot.py`: visualization tool for `datalog.csv` and `./results_csv`.
- `integrate_results.py`: convert latency/energy result to [aw_nas](https://github.com/walkerning/aw_nas) format.

## Steps to run compiled models

After compilation by Vitis-AI, we should get models in `.elf` file format. The `.elf` files should be placed in the `./elf` folder on the ZCU102 board.

First, you need to convert the `.elf` files into `.so` files, in order to run them. 

To do so, simply run:
```sh
$ python to_so.py
```
It does not have any dependency. The output `.so` files should be in the `./so` folder. 
**Then you need to copy the `.so` files into this folder: `/usr/lib`**

Second, run `./utils/build/latency` executable.

We prepared a simple C++ program to load the DPU kernel, run a few times, and save the layer-wise latency result to file. To run it:
```sh
$ ./utils/build/latency dpu_kernelname 100  >  latency_file.txt
```

## Power Profiling

Power profiling is to run all the compiled models in the `./so` folder, while recording the PL(Programmable Logic)'s power data. The power data is recorded with "Power Advantage Tool". 

To set up Power Advantage Tool, please consult this documentation: [Power Advantage Tool Setup Documentation](./doc_power.md).

The power profiling script should be executed on DPU board:
```sh
$ python3 power.py
```

## Latency Profiling

Latency profiling is the same process as power profiling.

The latency profiling script should be executed on DPU board:
```sh
$ python3 latency.py
```

## Parse Profiling Results

This process should be done on your own computer/server, instead of the DPU board.

### To segment the power data

The power data is recorded twice every second by the Power Advantage Tool. All the models are run sequentially, and their power data is recorded in the same `datalog.csv` file. So, we need to first segment each model's power data according to `test_time_stamps.txt`.

To do so, simply:
```sh
$ python divide_data.py
```

### To visualize power data

After the power data is segmented, we can plot them using:
```sh
$ python plot.py
```





