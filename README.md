# Introduction
- NFV platform for service chaining  

# Notification
- If you find any bugs or have some questions, please send an e-mail to us.  

# Configuration
- The configuration of the system: config/global.conf  
- The configurations of VNFs: config/vnf.conf  

# Test environment
- The current Probius is fully tested on Ubuntu 16.04.  
- It may work on other Linux platforms if its dependency issues are solved.  

# Installation
1. Set up a KVM environment  
$ cd setup   
$ ./kvm-install.sh  
$ ./ovs-install.sh  
$ sudo reboot  

2. Configure the KVM environment
$ cd setup
$ ./def-setup.sh  (change the IP space to 192.168.254.0/24)  
$ vi ovs-setup.sh  (update the interface names for inbound/outbound traffic)  
$ ./ovs-setup.sh  
$ ./ovs-into-kvm.sh  
$ sudo reboot

3. Create seven VMs  
$ virt-manager  
- VNFs: firewall, netsniff-ng, snort-ids, suricata-ids, suricata-ips, tcpdump, NAT
- Make sure that the name of new VMs are the above ones (case-sensitive)
- Use Ubuntu 16.04  
- Add two interfaces (attached to ovsbr0)  
- Statically Set the IP address of the first interface (ens3)
- (firewall: 192.168.254.11, netsniff-ng: 192.168.254.12, snort-ids: 192.168.254.13)  
- (suricata-ids: 192.168.254.14, suricata-ips: 192.168.254.15)  
- (tcpdump: 192.168.254.16, NAT: 192.168.254.17)  

4. Install VNF applications (run the following commands in VMs)  
$ git clone https://github.com/sdx4u/sfc  
$ ln -s sfc/apps/[VM name] [VM name]  
- follow the instruction in the README file  

# Execution
- Make a service chain  
$ ./sfc.py [VNF1,VNF2,VNF3,...]  

- Clean up the pre-installed service chain  
$ ./sfc.py clean  

# Author
- Jaehyun Nam <namjh@kaist.ac.kr>  
