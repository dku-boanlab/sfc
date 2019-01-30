#!/bin/bash

INBOUND=eth1
OUTBOUND=eth2

sudo iptables -F
sudo iptables -t nat -F

sudo ifconfig $INBOUND 0.0.0.0
sudo ifconfig $OUTBOUND 0.0.0.0

sudo ifconfig $INBOUND down
sudo ifconfig $OUTBOUND down
