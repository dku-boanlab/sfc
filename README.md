# Introduction
- NFV platform for service chaining  

# Notification
- If you find any bugs or have some questions, please send an e-mail to me.  

# Configuration
- The configuration of the platform: config/global.conf  
- The configurations of VNFs: config/vnf.conf  

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

# Test Scenario
1. Create default VMs  
$ virt-manager  
- VNFs: firewall, netsniff-ng, snort-ids, suricata-ids, suricata-ips, tcpdump, NAT  
- Make sure that the NAMEs of new VMs are the same with the above ones (case-sensitive)  

- Use Ubuntu 16.04 (image/ubuntu-16.04.2-server-amd64.iso)  
- Select 'NAT' network for the first (default) interface  
- Check 'customize configuration before installation' and add two more interfaces (Network source: ovsbr0)  
- During installation, statically set the IP address of the first interface (ens3) (DO NOT USE DHCP)  
- (firewall: 192.168.122.11, netsniff-ng: 192.168.122.12, snort-ids: 192.168.122.13)  
- (suricata-ids: 192.168.122.14, suricata-ips: 192.168.122.15, tcpdump: 192.168.122.16, NAT: 192.168.122.17)  
- Use 'ubuntu' for the user ID of default VMs  
- Check 'OpenSSH server' when selecting software to install  

- IF YOU WANT TO SAVE YOUR TIME, YOU CAN SIMPLY CREATE AND CONFIGURE ONE GENERAL VM  
- THEN, YOU CAN JUST CLONE AND RECONFIGURE IT FOR VNFS  
- Edit /etc/network/interfaces to change the pre-configured IP address  
- Edit /etc/hosts and /etc/hostname to change the hostname of the cloned VM)  

2. Push SSH keys to each VM in order to log it in without password  
$ util/push-key.sh ubuntu@[VM IP address]  
- (e.g., util/push-key.sh ubuntu@192.168.122.11)  

3. Install VNF applications (run the following commands in each VM)  
$ git clone https://github.com/sdx4u/sfc  
$ ln -s sfc/apps/[VM name]  
$ cd [VM name]  
$ ./setup.sh  
- Follow the instructions in the README file  

4. Make service chains as follows  
$ ./sfc.py snort-ids,NAT  
$ ./sfc.py firewall,suricata-ips,NAT  
$ ./sfc.py suricata-ids,netsniff-ng  

# Author
- Jaehyun Nam <namjh@kaist.ac.kr>  
