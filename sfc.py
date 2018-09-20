#!/usr/bin/python

import os
import sys
import json
import vnf_mgmt

def load_global_configurations(conf_file):
    config = {}

    with open(conf_file) as data_file:
        data = json.load(data_file)

        config["inbound"] = data["interface"]["inbound"]
        config["outbound"] = data["interface"]["outbound"]

        config["cpu"] = data["resource"]["cpu"]
        config["mem"] = data["resource"]["mem"]

    return config

list_VNFs = ""

if len(sys.argv) == 2:
    list_VNFs = sys.argv[1]
else:
    print "%s { list of VNFs (,) | clean }" % sys.argv[0]
    exit(0)

# load global configurations
g_config = load_global_configurations("config/global.conf")
print "Loaded global configurations"

# load VNF configurations
config = vnf_mgmt.load_VNF_configurations("config/vnf.conf")
print "Loaded VNF configurations"

# update VNF configurations
config = vnf_mgmt.update_VNF_configurations(config)
print "Updated VNF configurations"

# get the list of VNFs
VNFs = vnf_mgmt.get_the_list_of_VNFs(config)
print "Available VNFs in the config file: ", VNFs

# shut down the active VNFs
vnf_mgmt.shut_down_VNFs(VNFs)
print "Turned off all deployed VNFs"

# remove all applied flow rules
vnf_mgmt.initialize_Open_vSwitch(g_config)
print "Cleaned up all applied flow rules"

if sys.argv[1] == "clean":
    exit(0)

for vnf in list_VNFs.split(","):
    if vnf not in VNFs:
        print "Error: no " + vnf
        exit(0)

case = list_VNFs.split(",")

print "Service chain: ", case

# make the resources of VNFs
cpus, mems = vnf_mgmt.make_resources_VNFs(config, case)

print cpus
print mems

exit(0)

# get cpuset of VNFs
cpuset = vnf_mgmt.get_cpuset_of_VNFs(cpu, case)

# set cpus of VNFs
vnf_mgmt.set_cpus_of_VNFs(cpu, cpuset, case)

# set memories of VNFs
vnf_mgmt.set_mems_of_VNFs(mem, case)

# print the info of VNFs
for idx in range(len(case)):
    print case[idx], cpu[idx], mem[idx],
    print

# launch VNFs
vnf_mgmt.power_on_VNFs(config, VNFs)
print "Turned on VNFs"

# start applications
vnf_mgmt.start_applications_in_VNFs(config, VNFs)
print "Executed applications in VNFs"

# generate flow rules
rules = vnf_mgmt.make_the_chain_of_VNFs(config, VNFs)
print "Made flow rules for the chain of VNFs"

# add the flow rules
vnf_mgmt.apply_the_chain_of_VNFs(rules)
print "Applied the flow rules for the chain"
