#!/bin/bash

sudo rm -f ~/dump.pcap*

if [ -z $1 ]; then
	#sudo netsniff-ng -i ens4 -o ~/dump.pcap -s -J
	sudo netsniff-ng -i ens4 -o ~/dump.pcap -s -H -J -S 1GB
elif [ $1 == "b" ]; then
	#nohup sudo netsniff-ng -i ens4 -o ~/dump.pcap -s -J 0<&- &> ~/stats.log &
	nohup sudo netsniff-ng -i ens4 -o ~/dump.pcap -s -H -J -S 1GB 0<&- &> ~/stats.log &
fi
