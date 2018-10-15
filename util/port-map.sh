#!/bin/bash

# print the mapping of ports and interfaces
sudo ovs-ofctl show ovsbr0 | grep addr | grep -v LOCAL | awk -F"(" '{print "Port:" $1 " Interface: " $2}' | awk -F")" '{print $1}'
