import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import rcParams
from power_0826 import *


rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['DejaVu Serif']
names = ['timestamp', 'VCCINT', 'VCCBRAM', 'VCCAUX', 'VCC1V2'
         'VCC3V3', 'MGTAVCC', 'MGTAVTT', 'VCCPSINTFP', 'MGTRAVCC'
         'MGTRAVTT','VCCO_PSDDR_504', 'VCCPSDDRPLL']


def get_time_stamp():
    # read time stamp
    time_stamps = dict()
    with open('test_time_stamps.txt', 'r') as f:
        for line in f:
            net_name, start0, start1, end0, end1 = line.split(' ')
            end1 = end1.replace('\n', '')
            start = datetime.fromisoformat(start0 + ' ' + start1)
            end = datetime.fromisoformat(end0 + ' ' + end1)
            time_stamps[net_name] = [start, end]  
    return time_stamps               

def plot_all():
    filename = 'datalog.csv'

    time_stamps = get_time_stamp()

    table = dict()

    with open(filename, newline='') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for i, line in enumerate(lines):
            if i <= 1: continue
            for idx, string in enumerate(line):
                if idx > len(names) - 1: break
                name = names[idx]
                if name not in table.keys():
                    table[name] = list()
                if idx > 0: string = int(string)
                table[name].append(string)

    # import ipdb; ipdb.set_trace()            

    # plot vertical lines and write numbers on them
    # we only care vcc_int
    vcc_int = table['VCCINT']
    red_vertical_lines = dict() # netname : [start_iter, end_iter]
    for net_name, time_stamp in time_stamps.items():
        start, end = time_stamp
        for i, datum in enumerate(vcc_int):
            win_time_stamp = convert_time(table['timestamp'][i])
            if net_name not in red_vertical_lines.keys(): red_vertical_lines[net_name] = list()
            if win_time_stamp.minute == start.minute and win_time_stamp.second == start.second: 
                if len(red_vertical_lines[net_name]) >= 1: continue
                red_vertical_lines[net_name].append(i)
            if win_time_stamp.minute == end.minute and win_time_stamp.second == end.second:  
                if len(red_vertical_lines[net_name]) >= 2: continue
                red_vertical_lines[net_name].append(i)


    # import ipdb; ipdb.set_trace()

    plt.style.use('seaborn-paper')
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(10, 6)
    ax.autoscale(True)
    # draw data
    for label in names:
        if label == 'timestamp': continue
        data = table[label]
        length = len(data)
        ax.plot(range(length), data, label=label)
    # draw vertical lines
    for net_name, [start, end] in red_vertical_lines.items():
        plt.axvline(start, color='red', linestyle='--')
        plt.axvline(end, color='red', linestyle='--')

    # write the average figure on it
    for net_name, [start, end] in red_vertical_lines.items():
        avg = vcc_int[start:end]
        avg = sum(avg) / len(avg)
        avg = avg / 1e6
        avg = ' power: {:05.4f}(W)'.format(avg)
        avg = 'net: ' + net_name + avg
        ax.text(x=start+(end-start)/4, y=6.3*1e6, s=avg, fontsize=10)

    ax.set_xlabel('time steps', fontsize=15)
    ax.set_ylabel('value', fontsize=15)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right', prop={'size': 12}, ncol=1, bbox_to_anchor=(1, 0.8),
               frameon=True)

    plt.savefig("plot.png")


def plot_each():
    import os, shutil
    base_path = './results_plot'
    if os.path.exists(base_path):
        shutil.rmtree(base_path)
    os.mkdir(base_path)
    for _csv in os.listdir('./results_csv'):
        filename = _csv.replace('.csv', '')
        table = dict()
        _csv = os.path.join('./results_csv', _csv)
        with open(_csv, newline='') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            for i, line in enumerate(lines):
                if i <= 1: continue
                for idx, string in enumerate(line):
                    if idx > len(names) - 1: break
                    name = names[idx]
                    if name not in table.keys():
                        table[name] = list()
                    if idx > 0: string = int(string)
                    table[name].append(string)
        plt.style.use('seaborn-paper')
        fig, ax = plt.subplots(1, 1)
        fig.set_size_inches(10, 6)
        ax.autoscale(True)

        for label in names:
            if label == 'timestamp': continue
            data = table[label]
            length = len(data)
            ax.plot(range(length), data, label=label)
        ax.set_xlabel('time steps', fontsize=15)
        ax.set_ylabel('value', fontsize=15)
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper right', prop={'size': 12}, ncol=1, bbox_to_anchor=(1, 0.8),
                   frameon=True)
        full_path = os.path.join(base_path, filename + ".png")
        plt.savefig(full_path)


if __name__ == "__main__":
    plot_all()
    plot_each()
