#!/bin/bash

sudo kill -SIGINT `ps -ef | grep tcpdump | head -n 1 | awk '{print $2}'` 2> /dev/null
