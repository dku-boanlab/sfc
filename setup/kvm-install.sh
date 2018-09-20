#!/bin/bash

# install KVM hypervisor and tools to manage the hypervisor
sudo apt-get install -y qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils uuid \
                        linux-tools-common linux-tools-`uname -r` \
                        linux-tools-virtual virt-top virt-manager

# install psutil
sudo dpkg -i python-psutil_1.2.1-1ubuntu2_amd64.deb
