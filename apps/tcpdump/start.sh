#!/bin/bash

INBOUND=eth1

sudo rm -f ~/dump.pcap*

if [ -z $1 ]; then
	nohup sudo tcpdump -i $INBOUND -w ~/dump.pcap -n -s 65535 0<&- &> ~/stats.log &
else
	sudo tcpdump -i $INBOUND -w ~/dump.pcap -n -s 65535
fi
