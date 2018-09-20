#!/bin/bash

sudo ethtool -K ens4 gro off

sudo ifconfig ens4 promisc

sudo rm -rf /var/log/snort/*

if [ -z $1 ]; then
	sudo snort -i ens4 -c /etc/snort/snort.conf
elif [ $1 == "b" ]; then
	sudo snort -i ens4 -c /etc/snort/snort.conf -D
fi
