#!/bin/bash

# set-vcpu.sh [VNF name] [vCPU set (a-b / a,b)] [# of vCPUs]

LINE=`sudo grep -n vcpu /etc/libvirt/qemu/$1.xml | awk -F':' '{print $1}'`
HEAD=`expr $LINE - 1`
#NEW="  <vcpu placement='static' cpuset='$2'>$3</vcpu>"
NEW="  <vcpu placement='static'>$3</vcpu>"

sudo head -n $HEAD /etc/libvirt/qemu/$1.xml > $1.xml

echo "$NEW" >> $1.xml
TAIL=`sudo wc -l /etc/libvirt/qemu/$1.xml | awk '{print $1}'`
TAIL=`expr $TAIL - $LINE`

sudo tail -n $TAIL /etc/libvirt/qemu/$1.xml >> $1.xml

virsh define $1.xml > /dev/null

rm $1.xml
