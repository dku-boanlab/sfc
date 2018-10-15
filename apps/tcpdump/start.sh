#!/bin/bash

sudo rm -f ~/dump.pcap*

if [ -z $1 ]; then
	#sudo tcpdump -i ens4 -w ~/dump.pcap -n
	sudo tcpdump -i ens4 -w ~/dump.pcap -n -s 65535
elif [ $1 == "b" ]; then
	#nohup sudo tcpdump -i ens4 -w ~/dump.pcap -n  0<&- &> ~/stats.log &
	nohup sudo tcpdump -i ens4 -w ~/dump.pcap -n -s 65535 0<&- &> ~/stats.log &
fi
