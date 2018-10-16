#!/bin/bash

sudo iptables -F
sudo iptables -t nat -F

sudo ifconfig ens4 0.0.0.0
sudo ifconfig ens5 0.0.0.0

sudo ifconfig ens4 down
sudo ifconfig ens5 down
