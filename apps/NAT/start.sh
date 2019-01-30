#!/bin/bash

INBOUND=eth1
OUTBOUND=eth2

sudo ifconfig $INBOUND up
sudo ifconfig $OUTBOUND up

sudo ifconfig $INBOUND $1 netmask $2
sudo ifconfig $OUTBOUND $3 netmask $4

sudo iptables -t nat -A POSTROUTING -o $OUTBOUND -j MASQUERADE
sudo iptables -A FORWARD -i $INBOUND -o $OUTBOUND -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A FORWARD -i $OUTBOUND -o $INBOUND -j ACCEPT
