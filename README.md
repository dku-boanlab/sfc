# Introduction
- NFV platform for service chaining  

# Notification
- This platform works without any SDN controllers.  
- If you find any bugs or have some questions, please send an e-mail to me.  

# Configuration
- The configuration of the platform: config/global.conf  
- The configuration of VNFs: config/vnf.conf  

# Test environment
- The current platform is fully tested on Ubuntu 16.04.  
- It may work on other Linux platforms if its dependency issues are solved.  

# Installation
1. Set up a KVM environment  
$ cd setup  
$ ./sfc-install.sh  
$ sudo reboot  

2. Configure the KVM environment  
$ cd setup  
$ vi ovs-setup.sh (update interfaces for inbound/outbound traffic)  
$ ./ovs-setup.sh  
$ ./def-setup.sh (if you want to modify the default KVM network)  
$ ./download-ubuntu.sh (if you need the Ubuntu 16.04 image)  
$ sudo reboot  

3. Configure the interfaces for inbound/outbound traffic  
$ vi config/global.conf  

4. Configure VNFs  
$ vi config/vnf.conf (modify contents for your environment)  

# Execution
- Make a service chain  
$ ./sfc.py [VNF1,VNF2,VNF3,...]  

- Clean up the already-deployed service chain 
$ ./sfc.py clean 

- CAUSION! 
Please make sure that you have modified configuration files in the 'config' directory for your environment!!! 

# Test Scenario 1
1. Create default VMs in manual 
$ virt-manager  

- VNFs  
firewall, netsniff-ng, snort-ids, suricata-ids, suricata-ips, tcpdump, NAT  
Make sure that the NAMEs of new VMs are the same with the above ones (case-sensitive)  

- VM installation for each VNF  
Use Ubuntu 16.04 (~/images/ubuntu-16.04.2-server-amd64.iso)  
Select 'NAT' network for the first (default) interface  
Check 'customize configuration before installation' and add two more interfaces (network source: ovsbr0)  
During Ubuntu installation, set the static IP address for the first interface (DO NOT USE DHCP)  
Use the following ID and password (ID: ubuntu, PW: ubuntu)  
Check 'OpenSSH server' when selecting software to install  

- VNF IP addresses defined in the default configuration file  
firewall: 192.168.122.11  
netsniff-ng: 192.168.122.12  
snort-ids: 192.168.122.13  
suricata-ids: 192.168.122.14  
suricata-ips: 192.168.122.15  
tcpdump: 192.168.122.16  
NAT: 192.168.122.17  

2. Push SSH keys to each VM in order to log it in without password  
$ util/push-key.sh [user ID]@[VM IP address]  
(e.g., util/push-key.sh ubuntu@192.168.122.11)  

3. Install VNF applications (run the following commands in each VM)  
VM $ git clone https://github.com/sdx4u/sfc  
VM $ cd sfc/apps  
VM $ ./update.sh  
VM $ ./default-setup.sh  
VM $ sudo reboot  
VM $ ln -s sfc/apps/[VM name]  
VM $ cd [VM name]  
VM $ ./setup.sh  
Then, follow the instructions in the README file  

4. Make service chains as follows  
$ ./sfc.py snort-ids,NAT  
$ ./sfc.py firewall,suricata-ips,NAT  
$ ./sfc.py suricata-ids,netsniff-ng  

# Test Scenario 2
1. Create a general VM  
$ virt-manager  

- VM installation of the general VM  
Use Ubuntu 16.04 (~/images/ubuntu-16.04.2-server-amd64.iso)  
Select 'NAT' network for the first (default) interface  
Check 'customize configuration before installation' and add two more interfaces (network source: ovsbr0)  
During Ubuntu installation, set the static IP address for the first interface (192.168.122.10)  
Use the following ID and password (ID: ubuntu, PW: ubuntu)  
Check 'OpenSSH server' when selecting software to install  

2. Set default configurations  
$ ssh ubuntu@192.168.122.10  
VM $ git clone https://github.com/sdx4u/sfc  
VM $ cd sfc/apps  
VM $ ./update.sh  
VM $ ./default-setup.sh  
VM $ sudo reboot  
VM $ sudo vi /etc/sudoers  

> Add the following line at the end of the file  
> ubuntu	ALL=NOPASSWD:ALL  

VM $ sudo vi /etc/sysctl.conf  

> Uncomment the following line  
> net.ipv4.ip\_forward=1  

VM $ sudo vi /etc/network/interfaces  

> Add the following lines at the end of the file  
> auto eth1  
> iface eth1 inet manual  
> auto eth2  
> iface eth2 inet manual  

3. Install VNF applications  
$ ssh ubuntu@192.168.122.10  
VM $ ln -s sfc/apps/firewall  
VM $ cd firewall  
VM $ ./setup.sh  
VM $ cd ..  
VM $ ln -s sfc/apps/netsniff-ng  
VM $ cd netsniff-ng  
VM $ ./setup.sh  
VM $ cd ..  
VM $ ln -s sfc/apps/snort-ids  
VM $ cd snort-ids  
VM $ ./setup.sh  
VM $ cd ..  
VM $ ln -s sfc/apps/suricata-ids  
VM $ cd suricata-ids  
VM $ ./setup.sh  
VM $ cd ..  
VM $ ln -s sfc/apps/suricata-ips  
VM $ cd suricata-ips  
VM $ sudo cp config/suricata-ips.yaml /usr/local/etc/suricata/suricata-ips.yaml  
VM $ cd ..  
VM $ ln -s sfc/apps/tcpdump  
VM $ cd tcpdump  
VM $ ./setup.sh  
VM $ cd ..  
VM $ ln -s sfc/apps/NAT  
VM $ cd NAT  
VM $ ./setup.sh  

3. Clone the general VM for each VNF  
firewall, netsniff-ng, snort-ids, suricata-ids, suricata-ips, tcpdump, NAT  
Make sure that the NAMEs of new VMs are the same with the above ones (case-sensitive)  

4. Reconfigure cloned VMs for each VNF  
Repeat the following commands  
$ ssh ubuntu@192.168.122.10  
VM $ cd sfc/apps  
VM $ ./network-setup.sh [VNF] [VM IP address]  
(e.g., ./network-setup.sh firewall 192.168.122.11)  
VM $ sudo reboot  

5. Push SSH keys to each VM in order to log it in without password  
$ util/push-key.sh [user ID]@[VM IP address]  
(e.g., util/push-key.sh ubuntu@192.168.122.11)  

6. Make service chains as follows  
$ ./sfc.py snort-ids,NAT  
$ ./sfc.py firewall,suricata-ips,NAT  
$ ./sfc.py suricata-ids,netsniff-ng  

# Author
- Jaehyun Nam <namjh@kaist.ac.kr>  
