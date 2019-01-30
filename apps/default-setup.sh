#!/bin/bash

echo "LANGUAGE=en_US.UTF-8" | sudo tee -a /etc/environment
echo "LC_ALL=en_US.UTF-8" | sudo tee -a /etc/environment

sudo sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT=\"\"/GRUB_CMDLINE_LINUX_DEFAULT=\"net.ifnames=0 biosdevname=0\"/g' /etc/default/grub
sudo sed -i 's/GRUB_CMDLINE_LINUX=\"\"/GRUB_CMDLINE_LINUX=\"net.ifnames=0 biosdevname=0\"/g' /etc/default/grub

sudo update-grub2
