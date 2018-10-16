#!/usr/bin/python

import os
import math

STATS_LOG = "/usr/local/var/log/suricata/stats.log"

def get_seconds(tm):
    hms = tm.split(":")
    return (int(hms[0]) * 3600) + (int(hms[1]) * 60) + int(hms[2])

def get_difference(values):
    return [x - values[i - 1] for i, x in enumerate(values)][1:]

def get_median(values):
    tmp = []

    for value in values:
        tmp.append(value)

    tmp.sort()
    length = len(tmp)

    if length == 0:
        return 0.0

    median = length / 2

    if length % 2 == 1:
        return tmp[median]
    else:
        return ((tmp[median - 1] + tmp[median]) * 1.0) / 2

def get_stdev(values):
    tmp = []

    for value in values:
        tmp.append(value)

    tmp.sort()
    length = len(tmp)

    if length == 0:
        return 0.0

    avg = (sum(tmp) * 1.0) / length

    dev = []
    for x in tmp:
        dev.append(x - avg)

    sqr = []
    for x in dev:
        sqr.append(x * x)

    if len(sqr) <= 1:
        return 0.0

    mean = sum(sqr) / len(sqr)

    return math.sqrt(sum(sqr) / (len(sqr) - 1))

def get_median_filtered(values):
    if len(values) == 0:
        return 0.0

    tmp = []

    for value in values:
        tmp.append(value)

    tmp.sort()

    med_tmp = get_median(tmp)
    std_tmp = get_stdev(tmp)

    for t in tmp:
        if t < (med_tmp - (std_tmp * 0.34)):
            tmp.remove(t)
        elif t > (med_tmp + (std_tmp * 0.34)):
            tmp.remove(t)

    length = len(tmp)

    if length == 0:
        return 0.0

    median = length / 2

    if length % 2 == 1:
        return tmp[median]
    else:
        return ((tmp[median - 1] + tmp[median]) * 1.0) / 2

os.system("sync; sync; sync")

source = open(STATS_LOG, "r")
lines = source.read().splitlines()
source.close()

raw_times_inc = []
raw_frames_inc = []
raw_drops_inc = []
raw_packets_inc = []
raw_bytes_inc = []

raw_times = 0.0
raw_frames = 0.0
raw_drops = 0.0
raw_packets = 0.0
raw_bytes = 0.0

flag = 0
for index in range(len(lines)):
    line = lines[index].split()

    if line[0] == "Date:":
        raw_times = get_seconds(line[3])
        flag += 1
    if line[0] == "capture.kernel_packets":
        raw_frames = int(line[4]) * 1.0
        flag += 1
    elif line[0] == "capture.kernel_drops":
        raw_drops = int(line[4]) * 1.0
        flag += 1
    elif line[0] == "decoder.pkts":
        raw_packets = int(line[4]) * 1.0
        flag += 1
    elif line[0] == "decoder.bytes":
        raw_bytes = int(line[4]) * 1.0
        flag += 1

    if flag == 5:
        raw_times_inc.append(raw_times)
        raw_frames_inc.append(raw_frames)
        raw_drops_inc.append(raw_drops)
        raw_packets_inc.append(raw_packets)
        raw_bytes_inc.append(raw_bytes)

        raw_times = 0.0
        raw_frames = 0.0
        raw_drops = 0.0
        raw_packets = 0.0
        raw_bytes = 0.0

        flag = 0

time_diff = get_difference(raw_times_inc)
frames_diff = get_difference(raw_frames_inc)
drops_diff = get_difference(raw_drops_inc)
packets_diff = get_difference(raw_packets_inc)
bytes_diff = get_difference(raw_bytes_inc)

frames_end = []
drops_end = []
packets_end = []
bytes_end = []

delete = 0
for index in range(len(frames_diff)):
    if delete > 2 and frames_diff[index] > 0:
        frames_end.append(frames_diff[index] / time_diff[index])
        drops_end.append(drops_diff[index] / time_diff[index])
        packets_end.append(packets_diff[index] / time_diff[index])
        bytes_end.append(bytes_diff[index] / time_diff[index])

    delete += 1

f = get_median_filtered(frames_end)
d = get_median_filtered(drops_end)
p = get_median_filtered(packets_end)
b = get_median_filtered(bytes_end)

if f == 0.0:
    print 0.0, 0.0, 0.0
else:
    print p, b, d / f
