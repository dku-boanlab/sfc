import os
import time
import json
import psutil
import libvirt
import subprocess

def load_VNF_configurations(conf_file):
    config = {}

    with open(conf_file) as data_file:
        data = json.load(data_file)

        for name in data:
            config[name] = {}

            config[name]["name"] = str(name) # VNF name in a configuration
            config[name]["type"] = str(data[name]["type"]) # passive or inline

            config[name]["net0"] = "" # mgmt virtual interface
            config[name]["net1"] = "" # inbound virtual interface
            config[name]["net2"] = "" # outbound virtual interface

            config[name]["inbound"] = "" # inbound physical interface
            config[name]["outbound"] = "" # outbound physical interface

            config[name]["cpu"] = str(data[name]["cpu"]) # given number of CPUs (,)
            config[name]["mem"] = str(data[name]["mem"]) # given MEM size (,)

            config[name]["mgmt_ip"] = str(data[name]["mgmt_ip"]) # mgmt IP address

            config[name]["start"] = str(data[name]["start"]) # application start script
            config[name]["stop"] = str(data[name]["stop"]) # application stop script

            if "init" in data[name]:
                config[name]["init"] = str(data[name]["init"]) # VNF init script before/without NAT
            else:
                config[name]["init"] = ""

            if "nat_init" in data[name]:
                config[name]["nat_init"] = str(data[name]["nat_init"]) # VNF init script after NAT
            else:
                config[name]["nat_init"] = ""

    return config

def update_VNF_configurations(config):
    for process in psutil.process_iter():
        try:
            vnf = process.as_dict(attrs=['name', 'pid', 'cmdline'])
        except psutil.NoSuchProcess:
            pass

        for entry in vnf['cmdline']:
            if "qemu-system-x86_64" in entry or "qemu-kvm" in entry:
                name = vnf['cmdline'][vnf['cmdline'].index('-name') + 1]
                if name not in config:
                    print "%s is not in the VNF configurations" % (name)
                    continue

                for entry in vnf['cmdline']:
                    if "id=net" in entry:
                        options = entry.split(",")

                        id_option = options[2]
                        net_id = id_option.split("=")[1]

                        mac_option = options[3]
                        mac = mac_option.split("=")[1]

                        cmd = "virsh domiflist " + name + " | grep " + mac + " | awk '{print $1}'"
                        res = subprocess.check_output(cmd, shell=True)
                        intf = res.rstrip()

                        config[name][net_id] = intf

                # net0 is considered as mgmt interface
                config[name]["inbound"] = config[name]["net1"]
                config[name]["outbound"] = config[name]["net2"]

    return config

def get_list_of_VNFs(config):
    VNFs = []

    for name in config:
        VNFs.append(config[name]["name"])

    return VNFs

def make_resources_of_VNFs(g_config, config, VNFs):
    cpu_list = g_config["cpu"].split(',')
    mem_list = g_config["mem"].split(',')

    cpus = []
    count = pow(len(cpu_list), len(VNFs))

    for cnt in range(count):
        cpu_base = []
        for vnf in VNFs:
            cpu_base.append(0)
        cpus.append(cpu_base)

    for idx in range(len(VNFs)):
        cpus_idx = 0
        while cpus_idx < count:
            for cpu in cpu_list:
                loop_cnt = pow(len(cpu_list), len(VNFs) - idx - 1)
                for loop in range(loop_cnt):
                    vnf_cpu = config[VNFs[idx]]["cpu"].split(',')
                    if cpu in vnf_cpu:
                        cpus[cpus_idx][idx] = cpu
                    cpus_idx += 1

    final_cpus = []
    for cpu in cpus:
        if cpu not in final_cpus and 0 not in cpu:
            final_cpus.append(cpu)

    mems = []
    count = pow(len(mem_list), len(VNFs))

    for cnt in range(count):
        mem_base = []
        for vnf in VNFs:
            mem_base.append(0)
        mems.append(mem_base)

    for idx in range(len(VNFs)):
        mems_idx = 0
        while mems_idx < count:
            for mem in mem_list:
                loop_cnt = pow(len(mem_list), len(VNFs) - idx - 1)
                for loop in range(loop_cnt):
                    vnf_mem = config[VNFs[idx]]["mem"].split(',')
                    if mem in vnf_mem:
                        mems[mems_idx][idx] = mem
                    mems_idx += 1

    final_mems = []
    for mem in mems:
        if mem not in final_mems and 0 not in mem:
            final_mems.append(mem)

    return final_cpus, final_mems

def get_cpuset_of_VNFs(cpu, VNFs):
    cpuset = []

    cpu_list = []
    for v in cpu:
        cpu_list.append(int(v))

    total_cpus = int(os.sysconf('SC_NPROCESSORS_ONLN'))
    required_cpus = sum(cpu_list)

    for idx in range(len(cpu_list)):
        assigned_cpus = 0

        if idx == 0:
            assigned_cpus = 0
        else:
            for prev in range(len(cpu_list)):
                if prev < idx:
                    assigned_cpus += cpu_list[prev]
                else:
                    break

        if cpu_list[idx] == 1:
            start = assigned_cpus % total_cpus
            cpu_range = "%s" % (start)
            cpuset.append(cpu_range)
        else:
            start = assigned_cpus % total_cpus
            end = (assigned_cpus + int(cpu[idx]) - 1) % total_cpus
            if start < end:
                cpu_range = "%d-%d" % (start, end)
            else:
                cpu_range = "%d-%d,0-%d" % (start, total_cpus-1, end)
            cpuset.append(cpu_range)

    return cpuset

def set_cpus_of_VNFs(cpu, cpuset, VNFs):
    for idx in range(len(VNFs)):
        os.system("util/set-vcpu.sh %s %s %s" % (VNFs[idx], cpuset[idx], cpu[idx]))
        print "set-vcpu " + VNFs[idx] + " " + cpuset[idx] + " " + cpu[idx]

    return

def set_mems_of_VNFs(mem, VNFs):
    for idx in range(len(VNFs)):
        size = str(int(mem[idx]) * 1024)
        os.system("util/set-vmem.sh %s %s" % (VNFs[idx], size))
        print "set-vmem " + VNFs[idx] + " " + size

    return

def is_VNF_alive(mgmt_ip):
    res = os.system("ssh " + mgmt_ip + " exit 2> /dev/null")
    if res == 0:
        return True
    else:
        return False

def is_VNF_active(vnf):
    res = -1

    conn = libvirt.open("qemu:///system")
    if conn == None:
        print "Error: failed to connect QEMU"
        exit(-1)
    else:
        try:
            curr = conn.lookupByName(vnf)
            res = curr.isActive()
            conn.close()
        except libvirt.libvirtError:
            pass

    return res

def power_on_VNFs(config, VNFs):
    for vnf in VNFs:
        conn = libvirt.open("qemu:///system")
        if conn == None:
            print "Error: failed to connect QEMU"
            exit(-1)
        else:
            if is_VNF_active(vnf) == False:
                curr = conn.lookupByName(vnf)
                curr.create()
                conn.close()
            else: # True
                curr = conn.lookupByName(vnf)
                curr.destroy()

                time.sleep(1.0)

                curr.create()
                conn.close()

    for vnf in VNFs:
        power_on = False
        while power_on == False:
            if is_VNF_alive(config[vnf]["mgmt_ip"]):
                power_on = True

    return

def shut_down_VNFs(VNFs):
    filtered = []

    for vnf in VNFs:
        ret = is_VNF_active(vnf)

        if ret > 0:
            conn = libvirt.open("qemu:///system")
            if conn == None:
                print "Error: failed to connect QEMU"
                exit (-1)
            else:
                VNF = conn.lookupByName(vnf)
                VNF.destroy()
                conn.close()

        if ret >= 0:
            filtered.append(vnf)

    return filtered

def is_after_NAT(vnf, VNFs):
    ret = False

    for v in VNFs:
        if v == "NAT":
            ret = True
        elif v == vnf:
            break

    return ret

def start_applications_in_VNFs(config, VNFs):
    for vnf in VNFs:
        if is_after_NAT(vnf, VNFs):
            os.system("ssh " + config[vnf]["mgmt_ip"] + " " + config[vnf]["start"] + " " + config[vnf]["nat_init"])
        else:
            os.system("ssh " + config[vnf]["mgmt_ip"] + " " + config[vnf]["start"] + " " + config[vnf]["init"])

    return

def stop_applications_in_VNFs(config, VNFs):
    for vnf in VNFs:
        os.system("ssh " + config[vnf]["mgmt_ip"] + " " + config[vnf]["stop"])

    return

def get_port_from_intf(interface):
    cmd = "util/port-map.sh | grep " + interface + " | awk '{print $2}' | head -n 1"
    res = subprocess.check_output(cmd, shell=True)
    return res.rstrip()

def make_chain_of_VNFs(config, VNFs):
    rules = []

    vnf_cnt = 0
    out_port = ""

    rule = "sudo ovs-ofctl add-flow ovsbr0 in_port=1,actions="

    for vnf in VNFs:
        output = get_port_from_intf(config[vnf]["inbound"])

        if config[vnf]["type"] == "inline":
            out_port = get_port_from_intf(config[vnf]["outbound"])

        if config[vnf]["type"] == "inline":
            if vnf_cnt == 0:
                rule = rule + "output:" + output
            else:
                rule = rule + ",output:" + output

            vnf_cnt = 0
            rules.append(rule)

            rule = "sudo ovs-ofctl add-flow ovsbr0 in_port=" + out_port + ",actions="
        else: # passive
            if vnf_cnt == 0:
                rule = rule + "output:" + output
            else:
                rule = rule + ",output:" + output

            vnf_cnt = vnf_cnt + 1

    if vnf_cnt == 0:
        rule = rule + "output:2"
    else:
        rule = rule + ",output:2"

    rules.append(rule)

    rule = "sudo ovs-ofctl add-flow ovsbr0 in_port=2,actions="

    rev = []

    for vnf in VNFs:
        rev.append(vnf)

    rev.reverse()

    vnf_cnt = 0
    out_port = ""

    for vnf in rev:
        if config[vnf]["type"] == "inline":
            output = get_port_from_intf(config[vnf]["outbound"])
        else:
            output = get_port_from_intf(config[vnf]["inbound"])

        if config[vnf]["type"] == "inline":
            out_port = get_port_from_intf(config[vnf]["inbound"])

        if config[vnf]["type"] == "inline":
            if vnf_cnt == 0:
                rule = rule + "output:" + output
            else:
                rule = rule + ",output:" + output

            vnf_cnt = 0
            rules.append(rule)

            rule = "sudo ovs-ofctl add-flow ovsbr0 in_port=" + out_port + ",actions="
        else: # passive
            if vnf_cnt == 0:
                rule = rule + "output:" + output
            else:
                rule = rule + ",output:" + output

            vnf_cnt = vnf_cnt + 1

    if vnf_cnt == 0:
        rule = rule + "output:1"
    else:
        rule = rule + ",output:1"

    rules.append(rule)

    return rules

def initialize_Open_vSwitch(g_config):
    os.system("sudo ovs-vsctl del-br ovsbr0 2> /dev/null")
    os.system("sudo ovs-vsctl add-br ovsbr0")

    os.system("sudo ovs-vsctl set-controller ovsbr0 tcp:127.0.0.1:6633")
    os.system("sudo ovs-vsctl -- set bridge ovsbr0 protocols=OpenFlow10")
    os.system("sudo ovs-vsctl set-fail-mode ovsbr0 secure")

    os.system("sudo ovs-vsctl add-port ovsbr0 " + g_config["inbound"])
    os.system("sudo ovs-vsctl add-port ovsbr0 " + g_config["outbound"])

    return

def apply_chain_of_VNFs(rules):
    for rule in rules:
        os.system(rule)

    os.system("util/dump-flows.sh")

    return
