#!/bin/bash

sudo ifconfig ens4 up
sudo ifconfig ens5 up

sudo ifconfig ens4 $1 netmask $2
sudo ifconfig ens5 $3 netmask $4

sudo iptables -t nat -A POSTROUTING -o ens5 -j MASQUERADE
sudo iptables -A FORWARD -i ens4 -o ens5 -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A FORWARD -i ens5 -o ens4 -j ACCEPT

sudo iptables -t nat -A PREROUTING -p tcp -i ens4 --dport 80 -j DNAT --to 192.168.20.20:80
sudo iptables -t nat -A PREROUTING -p tcp -i ens4 --dport 5201 -j DNAT --to 192.168.20.20:5201
