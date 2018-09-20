#!/bin/bash

sudo apt-get update
sudo apt-get -y install ebtables bridge-utils
sudo modprobe br_netfilter
