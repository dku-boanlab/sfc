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

# Compilation
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

3. Create 7 default VNFs
$ virt-manager  
- VNFs: firewall, netsniff-ng, snort-ids, suricata-ids, suricata-ips, tcpdump, NAT
- Make sure that the name of new VMs are the above ones (case-sensitive)
- Use Ubuntu 16.04  
- Add two interfaces (attached to ovsbr0)  

# Execution
- Make a service chain  
$ ./sfc.py [VNF1,VNF2,VNF3,...]  

- Clean up the pre-installed service chain  
$ ./sfc.py clean  

# Author
- Jaehyun Nam <namjh@kaist.ac.kr>  
