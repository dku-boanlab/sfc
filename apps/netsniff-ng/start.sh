#!/bin/bash

INBOUND=eth1

sudo rm -f ~/dump.pcap*

if [ -z $1 ]; then
	nohup sudo netsniff-ng -i $INBOUND -o ~/dump.pcap -s -H -J 0<&- &> ~/stats.log &
else
	sudo netsniff-ng -i $INBOUND -o ~/dump.pcap -s -H -J
fi
