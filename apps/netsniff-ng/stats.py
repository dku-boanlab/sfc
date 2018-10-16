#!/usr/bin/python

import os
import time

os.system("/home/ubuntu/netsniff-ng/stop.sh")
os.system("sync; sync; sync")
time.sleep(1.0)

STATS_LOG = "/home/ubuntu/stats.log"

source = open(STATS_LOG, "r")
lines = source.read().splitlines()
source.close()

packets = 0.0
drops = 0.0

for line in lines:
    column = line.split()

    if "passed" in column:
        packets = int(column[0]) * 1.0
    elif "failed" in column:
        drops = int(column[0]) * 1.0

if (packets + drops) == 0.0:
    print 0.0, 0.0, 0.0
else:
    print packets, 0.0, drops / (packets + drops)

os.system("/home/ubuntu/netsniff-ng/start.sh b")
time.sleep(1.0)
