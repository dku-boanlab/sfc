#!/bin/bash

INBOUND=eth1
OUTBOUND=eth2

sudo brctl addbr br0
sudo brctl addif br0 $INBOUND
sudo brctl addif br0 $OUTBOUND
sudo brctl stp br0 off

sudo ifconfig br0 $1 netmask $2 up

/home/ubuntu/firewall/restore.sh
