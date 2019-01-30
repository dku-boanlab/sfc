#!/bin/bash

INBOUND=eth1
OUTBOUND=eth2

sudo ethtool -K $INBOUND gro off
sudo ethtool -K $OUTBOUND gro off

sudo rm -f /usr/local/var/run/suricata.pid
sudo rm -rf /usr/local/var/log/suricata/*

if [ -z $1 ]; then
	sudo suricata -c /usr/local/etc/suricata/suricata-ips.yaml --af-packet
elif [ $1 == "b" ]; then
	sudo suricata -c /usr/local/etc/suricata/suricata-ips.yaml --af-packet -D
fi
