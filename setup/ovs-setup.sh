#!/bin/bash

# remove and add ovsbr0
sudo ovs-vsctl del-br ovsbr0 2> /dev/null
sudo ovs-vsctl add-br ovsbr0

# configure ovsbr0
sudo ovs-vsctl set-controller ovsbr0 tcp:127.0.0.1:6633
sudo ovs-vsctl -- set bridge ovsbr0 protocols=OpenFlow10
sudo ovs-vsctl set-fail-mode ovsbr0 secure

# add interfaces to ovsbr0
sudo ovs-vsctl add-port ovsbr0 ens4
sudo ovs-vsctl add-port ovsbr0 ens6

# add ovsbr0 to KVM
virsh net-define ovsbr0.xml
virsh net-start ovsbr0
virsh net-autostart ovsbr0
