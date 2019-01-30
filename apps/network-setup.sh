#!/bin/bash

if [ -z $1 ]; then
	echo "$0 [hostname] [IP address]"
	exit
elif [ -z $2 ]; then
	echo "$0 [hostname] [IP address]"
	exit
fi

# change hostname
sudo sed -i 's/ubuntu/'$1'/g' /etc/hosts
sudo sed -i 's/ubuntu/'$1'/g' /etc/hostname

# change IP address
sudo sed -i 's/192.168.122.10/'$2'/g' /etc/network/interfaces
