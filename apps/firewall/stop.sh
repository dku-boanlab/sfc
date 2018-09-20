#!/bin/bash

/home/ubuntu/firewall/backup.sh

sudo ifconfig br0 0.0.0.0 down

sudo brctl delbr br0
