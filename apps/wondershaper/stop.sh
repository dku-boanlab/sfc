#!/bin/bash

sudo wondershaper remove br0

sudo ifconfig br0 0.0.0.0 down

sudo brctl delbr br0
