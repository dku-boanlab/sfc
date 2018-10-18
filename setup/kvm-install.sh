#!/bin/bash

sudo apt-get install -y qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils uuid \
                        linux-tools-common linux-tools-`uname -r` \
                        linux-tools-virtual virt-top virt-manager
