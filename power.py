"""
This script is for power measuring with OFA
and mobilenet networks. It does three things:
1. run the compiled networks (in .so library format) one by one
2. wait a moment in between each run
3. record the start and end time stamp for each run
"""
import csv
import os
from datetime import datetime
from time import sleep
from tqdm import tqdm

months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}

latency_binary = '/home/root/niansong/auto_deploy/utils/build/latency'


def run(so_name='libdpumodelfpga10.so', time=1000):
    kernel_name = so_name.replace('libdpumodel', '')
    kernel_name = kernel_name.split('/')[-1]
    kernel_name = kernel_name.split('.')[0]
    # kernel_name = kernel_name + "_0"
    cmd = latency_binary + " " + kernel_name + " " + str(time) + " > " + './latency/' +kernel_name + ".txt"
    # don't need latency for this time
    # cmd = latency_binary + " " + kernel_name + " " + str(time) + " > /dev/null"
    
    print(cmd)
    
    start = datetime.now()
    os.system(cmd)
    end = datetime.now()
    return kernel_name, start, end


def run_power_profiling():
    kernels = os.listdir('./so')
    import glob
    # kernels = glob.glob('/usr/lib/libdpumodelsample*')
    print("preparing...")
    sleep(5)
    time_stamps = list()
    for kernel in tqdm(kernels):
        # net0, net1 run number option
        times = 1000
        if 'net0' in kernel:
            times = 2000
        elif 'net1' in kernel:
            times = 10000
        kernel_name, start, end = run(kernel, times)
        print("waiting...")
        sleep(2)
        net_name = kernel_name
        time_stamps.append([net_name, start, end])
    print("done")

    # write time stamp file
    with open('test_time_stamps.txt', 'w') as f:
        for test_run in time_stamps:
            net_name, start, end = test_run
            f.write("{} {} {}\n".format(net_name, start, end))



if __name__ == "__main__":
    run_power_profiling()
