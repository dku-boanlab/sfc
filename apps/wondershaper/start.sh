#!/bin/bash

INBOUND=eth1
OUTBOUND=eth2

sudo brctl addbr br0
sudo brctl addif br0 $INBOUND
sudo brctl addif br0 $OUTBOUND
sudo brctl stp br0 off

sudo ifconfig br0 $1 netmask $2 up

if [ -z $3 ]; then
    sudo wondershaper br0 1048576 1048576
    echo "Wondershaper queues have been limited (TX 1GB, RX 1GB)"
else
    sudo wondershaper br0 $3 $4
    echo "Wondershaper queues have been limited (TX $3KB, RX $4KB)"
fi
