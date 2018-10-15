#!/bin/bash

sudo brctl addbr br0
sudo brctl addif br0 ens4
sudo brctl addif br0 ens5
sudo brctl stp br0 off

sudo ifconfig br0 $1 netmask $2 up

/home/ubuntu/firewall/restore.sh
