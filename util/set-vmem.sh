#!/bin/bash

# set-vmem.sh [VNF name] [memory size (KB)]

LINE=`sudo grep -n memory /etc/libvirt/qemu/$1.xml | awk -F':' '{print $1}'`
HEAD=`expr $LINE - 1`

sudo head -n $HEAD /etc/libvirt/qemu/$1.xml > $1.xml

NEW="  <memory unit='KiB'>$2</memory>"
echo "$NEW" >> $1.xml
NEW="  <currentMemory unit='KiB'>$2</currentMemory>"
echo "$NEW" >> $1.xml
TAIL=`sudo wc -l /etc/libvirt/qemu/$1.xml | awk '{print $1}'`
LINE=`expr $LINE + 1`
TAIL=`expr $TAIL - $LINE`

sudo tail -n $TAIL /etc/libvirt/qemu/$1.xml >> $1.xml

virsh define $1.xml > /dev/null

rm $1.xml
