import csv
import os
from datetime import datetime, timezone, timedelta
from time import sleep

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
LA_timezone = timezone(timedelta(hours=-8)) # ZCU102 timezone is America/Los_Angeles
BJ_timezone = timezone(timedelta(hours=8))  # windows computer's timezone is Asia/Shanghai

def convert_time(string='Sat Jul 25 21:04:36 2020'):
    """
    convert time format
    :return: a datetime object
    """
    _, month, day, time, year = string.split(" ")
    month = months[month]
    day = int(day)
    hour, min, sec = [int(item) for item in time.split(':')]
    year = int(year)

    # my time stamp was in wrong timezone
    # hour -= 16
    # if hour < 0: day -= 1
    # hour = hour % 24
    return datetime(year=year, month=month, day=day, hour=hour, minute=min, second=sec, tzinfo=LA_timezone).astimezone(BJ_timezone)


def divide_power_data():
    """
    cut `datalog.csv` according to time stamps,
    and save them to smaller csv files
    """
    # read time stamp
    time_stamps = dict()
    with open('test_time_stamps.txt', 'r') as f:
        for line in f:
            net_name, start0, start1, end0, end1 = line.split(' ')
            end1 = end1.replace('\n', '')
            start = datetime.fromisoformat(start0 + ' ' + start1).astimezone(BJ_timezone)
            end = datetime.fromisoformat(end0 + ' ' + end1).astimezone(BJ_timezone)
            time_stamps[net_name] = [start, end]
    # read csv
    whole_data = []
    legend = []
    with open('datalog.csv', newline='') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for i, line in enumerate(lines):
            if i == 0: legend = line
            else: whole_data.append(line)
    collection = dict()
    # cut the data in parts
    for name, time_stamp in time_stamps.items():
        start, end = time_stamp
        for line in whole_data:
            win_time_stamp = convert_time(line[0])
#            print("this={}, start={}, end={}, in={}".format(
#                 win_time_stamp, start, end,
#                 (win_time_stamp >= start and win_time_stamp <= end)
#             ))
            if win_time_stamp < start: continue
            if win_time_stamp > end: continue
            print("this={}, start={}, end={}, in={}".format(
                 win_time_stamp, start, end,
                (win_time_stamp >= start and win_time_stamp <= end)
             ))
            if name not in collection.keys():
                collection[name] = list()
            collection[name].append(line)
    # write out csv files
    base_path = './results_csv'
    if os.path.exists(base_path):
        import shutil
        shutil.rmtree(base_path)
    os.mkdir(base_path)
    for orig_name, data in collection.items():
        full_path = os.path.join(base_path, orig_name+'.csv')
        # write to one csv file
        with open(full_path, 'w', newline='') as csvfile:
            wr = csv.writer(csvfile, delimiter=',')
            # write lines
            wr.writerow(legend)
            for line in collection[orig_name]:
                wr.writerow(line)

if __name__ == "__main__":
    divide_power_data()
