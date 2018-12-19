#!/bin/bash

#install kvm
sudo apt-get install -y qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils uuid \
                        linux-tools-common linux-tools-`uname -r` \
                        linux-tools-virtual virt-top virt-manager

# install open vswitch
sudo apt-get install -y openvswitch-switch
