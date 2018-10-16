#!/usr/bin/python

import os
import time

os.system("/home/ubuntu/tcpdump/stop.sh")
os.system("sync; sync; sync")
time.sleep(1.0)

STATS_LOG = "/home/ubuntu/stats.log"

source = open(STATS_LOG, "r")
lines = source.read().splitlines()
source.close()

captured = 0.0
received = 0.0
dropped = 0.0

for line in lines:
    column = line.split()

    if "captured" in column:
        captured = int(column[0]) * 1.0
    elif "received" in column:
        received = int(column[0]) * 1.0
    elif "dropped" in column:
        drops = int(column[0]) * 1.0

if (received + dropped) == 0.0:
    print 0.0, 0.0, 0.0
else:
    print captured, 0.0, dropped / (received + dropped)

os.system("/home/ubuntu/tcpdump/start.sh b")
time.sleep(1.0)
