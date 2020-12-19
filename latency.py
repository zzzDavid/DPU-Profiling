import csv
import os
from datetime import datetime
from time import sleep
from tqdm import tqdm


latency_binary = '/home/root/niansong/auto_deploy/utils/build/latency'


def run(so_name='libdpumodelfpga10.so', time=1000):
    kernel_name = so_name.replace('libdpumodel', '')
    kernel_name = kernel_name.split('/')[-1]
    kernel_name = kernel_name.split('.')[0]
    # kernel_name = kernel_name + "_0"
    cmd = latency_binary + " " + kernel_name + " " + str(time) + " > " + './latency/' +kernel_name + ".txt"
    
    print(cmd)
    
    start = datetime.now()
    os.system(cmd)
    end = datetime.now()
    return kernel_name, start, end


def run_profiling():
    kernels = os.listdir('./so')
    import glob
    print("preparing...")
    sleep(5)
    time_stamps = list()
    for kernel in tqdm(kernels):
        times=1000
        kernel_name, start, end = run(kernel, times)
        print("waiting...")
        sleep(2)
        net_name = kernel_name
        time_stamps.append([net_name, start, end])
    print("done")



if __name__ == "__main__":
    run_profiling()
