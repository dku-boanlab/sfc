#!/bin/bash

# stop the default network
virsh net-destroy default

# edit the default network
virsh net-edit default

# start the default network
virsh net-start default

# set the autostart of the default network
virsh net-autostart default
