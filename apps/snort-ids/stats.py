#!/usr/bin/python

import os
import math

STATS_LOG = "/var/log/snort/snort.stats"

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

raw_packets = []
raw_bytes = []

raw_recv = []
raw_drop = []

delete = 0
for line in lines:
    if line[0] == "#":
        continue

    data = line.split(",")

    packets_sec = float(data[4]) * 1000
    bytes_sec = packets_sec * float(data[5])

    recv_sec = float(data[45])
    drop_sec = float(data[46])

    if delete > 2:
        raw_packets.append(packets_sec)
        raw_bytes.append(bytes_sec)

        raw_recv.append(recv_sec)
        raw_drop.append(drop_sec)

    delete += 1

p = get_median_filtered(raw_packets)
b = get_median_filtered(raw_bytes)
r = get_median_filtered(raw_recv)
d = get_median_filtered(raw_drop)

if r == 0.0:
    print 0.0, 0.0, 0.0
else:
    print p, b, d / r
