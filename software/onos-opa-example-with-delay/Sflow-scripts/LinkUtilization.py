#!/usr/bin/env python
from __future__ import print_function
from __future__ import unicode_literals
import subprocess
from json import loads
from utils import json_get_req
import dataStorage as ds
import vals


def get_switch(switches_list, ifname):
    for switch1 in switches_list:
        if ifname == switch1.ifName:
            return switch1


def if_all_switches_have_name(switches):
    for switch1 in switches:
        if switch1.ifName == "no_name_yet":
            return False
    return True


def print_ports_and_headers(src_losses, dst_losses):
    for key in src_losses.keys():
        print("\t{}\t\t".format(key), end='')
    for key in dst_losses.keys():
        print("\t{}\t\t".format(key), end='')
    print('')

    counter = len(src_losses.keys()) + len(dst_losses.keys())
    for i in range(0, counter):
        print("KB/s in\t\tKB/s out\t", end='')
    print('')


def print_loss_on_ports(src_losses, dst_losses, ports_and_headers_printed):
    if not ports_and_headers_printed:
        print_ports_and_headers(src_losses, dst_losses)

    for value in src_losses.values():
        print("{}\t{}\t".format(value, value), end='')
    for value in dst_losses.values():
        print("{}\t{}\t".format(value, value), end='')
    print('')


def get_loss_on_links_manual(switches, ports_and_headers_printed):
    # print("Retrieving Links...")
    reply = json_get_req('http://127.0.0.1:8181/onos/v1/links')
    src_losses = {}
    dst_losses = {}
    for link in reply['links']:
        src_node = link['src']['device']
        dst_node = link['dst']['device']
        src_port_number = link['src']['port']
        dst_port_number = link['dst']['port']

        src_switch_name = ''
        dst_switch_name = ''
        src_port = json_get_req('http://127.0.0.1:8181/onos/v1/devices/%s/ports' % src_node)
        for port in src_port['ports']:
            if port['port'] == src_port_number:
                src_switch_name = port['annotations']['portName']
        dst_port = json_get_req('http://127.0.0.1:8181/onos/v1/devices/%s/ports' % dst_node)
        for port in dst_port['ports']:
            if port['port'] == dst_port_number:
                dst_switch_name = port['annotations']['portName']

        src_switch = get_switch(switches, src_switch_name[0:3])
        dst_switch = get_switch(switches, dst_switch_name[0:3])
        src_bytes = 0
        dst_bytes = 0

        # print("switches len: {}".format(len(switches)))
        if src_switch is not None and dst_switch is not None:
            if len(src_switch.flows) > 0 and len(dst_switch.flows) > 0:
                # print("src_switch_len: {} dst_switch_len {}".format(len(src_switch.flows), len(dst_switch.flows)))
                for src_flow in src_switch.flows:
                    for dst_flow in dst_switch.flows:
                        if src_flow.id == dst_flow.id and src_flow.src_ip != vals.return_flows_src_address and \
                                dst_flow.src_ip != vals.return_flows_src_address:
                        # if src_flow.id == dst_flow.id:
                            src_bytes += src_flow.bytes_registered
                            dst_bytes += dst_flow.bytes_registered
                            # print("srcflow: {} dst_flow {} srcBytes {} dstbytes {}".format(src_flow.id, dst_flow.id, src_bytes, dst_bytes))

        loss = src_bytes - dst_bytes
        if loss != 0 and src_bytes != 0:
            loss = float(loss / src_bytes) * 100
        if loss < 0:
            loss = 0
        # if src_bytes != 0 and dst_bytes != 0 and loss >= 0:
            # print("Loss on link {}-{} totals {} percent".format(src_switch_name, dst_switch_name, loss))
        src_losses[src_switch_name] = loss
        dst_losses[dst_switch_name] = loss

    print_loss_on_ports(src_losses, dst_losses, ports_and_headers_printed)


ifInOctets = ""
ifOutOctets = ""
InOctetTime = 0
OutOctetTime = 0
p = subprocess.Popen(
    ['/usr/local/bin/sflowtool', '-j'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)
List1 = []
List2 = []
List3 = []
lines = iter(p.stdout.readline, '')
switch_dict_in = {}
switch_dict_out = {}
switch_names = {}
switches = []
flow_id_counter = 0
current_time = 0
ports_and_headers_printed = False
errorLogs = open("errorLogs.txt", "w")

first_loop = True
full_cycle = False
first_switch_name = ''

for line in lines:
    datagram = loads(line)
    sysUpTime = int(datagram["sysUpTime"])
    samples = datagram["samples"]
    currentAgentSubId = datagram["agentSubId"]

    if currentAgentSubId not in switch_names:
        switch_names[currentAgentSubId] = "no_name_yet"
        switches.append(ds.Switch("no_name_yet", currentAgentSubId))

    for sample in samples:
        sampleType = sample["sampleType"]
        elements = sample["elements"]
        if sampleType == "FLOWSAMPLE":  # ================ Flowsample
            try:
                srcIP = elements[1]["srcIP"]
                dstIP = elements[1]["dstIP"]
                bytes_reg = elements[1]["sampledPacketSize"]
                if currentAgentSubId in switch_names:  # dodawanie bajtow do konkretnego flowa na konkretnym switchu
                    index = list(switch_names).index(currentAgentSubId)
                    switches[index].add_bytes_to_flow(srcIP, dstIP, bytes_reg)
            except:
                errorLogs.write("no src/dst IP")

        if sampleType == "COUNTERSSAMPLE":  # ================ Countersample
            for element in elements:
                tag = element["counterBlock_tag"]
                if tag == "0:1005":
                    if first_loop:
                        first_switch_name = elements[2]["ifName"]
                    if first_switch_name == elements[2]["ifName"] and not first_loop:
                        full_cycle = True

                    ifName = elements[2]["ifName"]

                    if switch_names[currentAgentSubId] == "no_name_yet":
                        switch_names[currentAgentSubId] = ifName[0:3]
                        for switch in switches:
                            if switch.agentSubId == currentAgentSubId and switch.ifName == "no_name_yet":
                                switch.ifName = ifName[0:3]
                                break

                    first_loop = False
                    full_cycle = False
    if sysUpTime != current_time:
        current_time = sysUpTime
        # print("sysUpTime: {}".format(sysUpTime))
        # for switch in switches:
        #     switch.print_switch()
        if if_all_switches_have_name(switches):
            get_loss_on_links_manual(switches, ports_and_headers_printed)
            if not ports_and_headers_printed:
                ports_and_headers_printed = True

errorLogs.close()
