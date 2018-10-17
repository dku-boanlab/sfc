#!/bin/bash

sudo apt-get update
sudo apt-get -y install build-essential libpcap-dev libpcre3-dev libdumbnet-dev bison flex ethtool python

cd snort_src
rm -rf daq-2.0.6 nghttp2-1.17.0 snort-2.9.9.0

tar xvfz daq-2.0.6.tar.gz
cd daq-2.0.6
./configure
make
sudo make install
cd ..
rm -rf daq-2.0.6

sudo apt-get install -y zlib1g-dev liblzma-dev openssl libssl-dev

tar xvfz nghttp2-1.17.0.tar.gz
cd nghttp2-1.17.0
autoreconf -i --force
automake
autoconf
./configure --enable-lib-only
make
sudo make install
cd ..
rm -rf nghttp2-1.17.0

tar xvfz snort-2.9.9.0.tar.gz
cd snort-2.9.9.0
./configure --enable-sourcefire --enable-perfprofiling --enable-ppm
make
sudo make install
sudo ldconfig

grep snort /etc/group
if [ $? == 1 ]; then
	sudo groupadd snort
fi

grep snort /etc/passwd
if [ $? == 1 ]; then
	sudo useradd snort -r -s /sbin/nologin -c SNORT_IDS -g snort
fi

sudo rm -rf /usr/sbin/snort
sudo ln -s /usr/local/bin/snort /usr/sbin/snort

sudo rm -rf /etc/snort
sudo mkdir /etc/snort
sudo mkdir /etc/snort/rules
sudo mkdir /etc/snort/rules/iplists
sudo mkdir /etc/snort/preproc_rules
sudo mkdir /etc/snort/so_rules

sudo rm -rf /usr/local/lib/snort_dynamicrules
sudo mkdir /usr/local/lib/snort_dynamicrules

sudo touch /etc/snort/rules/iplists/black_list.rules
sudo touch /etc/snort/rules/iplists/white_list.rules
sudo touch /etc/snort/rules/local.rules
sudo touch /etc/snort/sid-msg.map

sudo rm -rf /var/log/snort
sudo mkdir /var/log/snort
sudo mkdir /var/log/snort/archived_logs

sudo chmod -R 5775 /etc/snort
sudo chmod -R 5775 /var/log/snort
sudo chmod -R 5775 /var/log/snort/archived_logs
sudo chmod -R 5775 /etc/snort/so_rules
sudo chmod -R 5775 /usr/local/lib/snort_dynamicrules

sudo chown -R snort:snort /etc/snort
sudo chown -R snort:snort /var/log/snort
sudo chown -R snort:snort /usr/local/lib/snort_dynamicrules

cd etc
sudo cp *.conf* /etc/snort
sudo cp *.map /etc/snort
sudo cp *.dtd /etc/snort
cd ..

cd src/dynamic-preprocessors/build/usr/local/lib/snort_dynamicpreprocessor
sudo cp * /usr/local/lib/snort_dynamicpreprocessor
cd ../../../../../../../..
rm -rf snort-2.9.9.0

tar xvfz snortrules-snapshot-2990.tar.gz
sudo cp -r preproc_rules/* /etc/snort/preproc_rules/
sudo cp -r rules/* /etc/snort/rules/
sudo cp -r so_rules/* /etc/snort/so_rules/
sudo cp -r etc/* /etc/snort/
sudo rm -rf preproc_rules rules so_rules etc

cd ../etc
sudo cp /etc/snort/snort.conf /etc/snort/snort.conf.bak
sudo cp snort.conf /etc/snort/snort.conf
