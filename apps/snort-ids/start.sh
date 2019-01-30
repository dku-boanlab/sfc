#!/bin/bash

INBOUND=eth1

sudo ethtool -K $INBOUND gro off
sudo ifconfig $INBOUND promisc

sudo rm -rf /var/log/snort/*

if [ -z $1 ]; then
	sudo snort -i $INBOUND -c /etc/snort/snort.conf -D
else
	sudo snort -i $INBOUND -c /etc/snort/snort.conf
fi
