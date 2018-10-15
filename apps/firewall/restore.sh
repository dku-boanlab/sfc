#!/bin/bash

# reconfigure the previous rules
sudo iptables-restore < /home/ubuntu/firewall/rules
