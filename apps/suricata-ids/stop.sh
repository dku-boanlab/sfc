#!/bin/bash

sudo kill -SIGINT `ps -ef | grep suricata | head -n 1 | awk '{print $2}'` 2> /dev/null
sudo rm -f /usr/local/var/run/suricata.pid
