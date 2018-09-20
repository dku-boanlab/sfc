#!/bin/bash

sudo kill -SIGINT `ps -ef | grep netsniff-ng | head -n 1 | awk '{print $2}'` 2> /dev/null
