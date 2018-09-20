#!/bin/bash

virsh net-define ovsbr0.xml
virsh net-start ovsbr0
virsh net-autostart ovsbr0
