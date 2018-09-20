#!/bin/sh

i=0
nproc=`nproc`

if [ $# -eq 0 ]
then
    echo "====================== HOW TO USE ======================"
    echo "$0 [0:check status,1:performance,2:powersave]"
    echo "========================================================"
else
    # check status
    if [ $1 -eq 0 ]
    then
        while [ $i -lt $(nproc) ]
        do
            sudo echo "CPU$i:" `cat /sys/devices/system/cpu/cpu$i/cpufreq/scaling_governor`
            i=`expr $i + 1`
        done
    # performance mode
    elif [ $1 -eq 1 ]
    then
        while [ $i -lt $(nproc) ]
        do
            echo performance | sudo tee /sys/devices/system/cpu/cpu$i/cpufreq/scaling_governor > /dev/null
            sudo echo "CPU$i:" `cat /sys/devices/system/cpu/cpu$i/cpufreq/scaling_governor`
            i=`expr $i + 1`
        done
    # powersave mode
    elif [ $1 -eq 2 ]
    then
        while [ $i -lt $(nproc) ]
        do
            echo powersave | sudo tee /sys/devices/system/cpu/cpu$i/cpufreq/scaling_governor > /dev/null
            sudo echo "CPU$i:" `cat /sys/devices/system/cpu/cpu$i/cpufreq/scaling_governor`
            i=`expr $i + 1`
        done
    # input error
    else
        echo "Input error!"
    fi
fi
