#!/bin/bash

sudo iptables -t nat -F
sudo iptables -F

sudo ifconfig ens4 0.0.0.0
sudo ifconfig ens5 0.0.0.0

sudo ifconfig ens4 down
sudo ifconfig ens5 down
