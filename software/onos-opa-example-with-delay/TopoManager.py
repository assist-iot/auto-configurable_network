import matplotlib.pyplot as plt
import networkx as nx
from config import *
from utils import json_get_req
import logging
import subprocess
import threading


class TopoManager(object):
    def __init__(self):
        self.G = nx.DiGraph()
        self.pos = None
        self.hosts = []
        self.devices = []
        self.deviceId_to_chassisId = {}

# MR collect loss
        self.losses = {}
# MZ collect ifstat
        self.usage = {}
        self.delay = {}
        x = threading.Thread(target=self.ifstat_loop, args=('ifstat',))
        x.start()
        y = threading.Thread(target=self.ifstat_loop, args=('/home/mich/Downloads/emu-230417/onos-opa-example/mainsflow.sh',))
        y.start()
        y = threading.Thread(target=self.ifstat_loop, args=('/home/mich/Downloads/emu-230417/onos-opa-example/delay.sh',))
        

        self.retrieve_topo_from_ONOS()

# MZ collect ifstat
    def ifstat_loop(self,name):
        interfaces = []
        ifstat_process = subprocess.Popen(name, stdout=subprocess.PIPE)
        while True:
            output = ifstat_process.stdout.readline()
            if output == '' and ifstat_process.poll() is not None:
                break
            if output:
                temp = output.decode("utf-8").split()
                #if name == './mainsflow.sh':
                #    print(temp)
                if len(interfaces) == 0:
                    interfaces = temp
                else:
                    #if name == './mainsflow.sh':
                    #    print(interfaces)
                    if 's' in temp[0]:
                        continue
                    for i in range(len(interfaces)):
                        if name == 'ifstat':
                            self.usage[interfaces[i]] = float(temp[i*2 + 1])*150.0
                        else:
                            if name == './mainsflow.sh':
                                self.losses[interfaces[i]] = float(temp[i*2 + 1])
                            else:
                                self.delay[interfaces[i]] = float(temp[i*2 + 1])
#            self.losses = sedlf.usage
#            print(self.usage)

    def retrieve_topo_from_ONOS(self):
        logging.info("Retrieving Topology...")
        reply = json_get_req('http://%s:%d/onos/v1/devices' % (ONOS_IP, ONOS_PORT))
        if 'devices' not in reply:
            return
        for dev in reply['devices']:
            # id is 'of:00000000000000a1', chassisID is 'a1'
            self.deviceId_to_chassisId[dev['id']] = dev['chassisId']
            self.G.add_node(dev['id'], type='device')
            self.devices.append(dev['id'])             

# MZ collect bandwidth
        cmd = ['sudo', 'ovs-vsctl', 'list', 'interface']
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        ingress_policing_rate = 0
        rates = {}
        for line in result.stdout.splitlines():
            temp=line.split()
            if len(temp) == 2 and temp[0] == b'ingress_policing_rate:':
                ingress_policing_rate = int(temp[1])
            if len(temp) == 3 and temp[0] == b'name':
                rates[temp[2].decode("utf-8")] = 50000


        reply = json_get_req('http://%s:%d/onos/v1/links' % (ONOS_IP, ONOS_PORT))
        if 'links' not in reply:
            return
        for link in reply['links']:
            src_node = link['src']['device']
            dst_node = link['dst']['device']
            src_port_number = link['src']['port']
            dst_port_number = link['dst']['port']
            port_reply = json_get_req('http://%s:%d/onos/v1/devices/%s/ports' % (ONOS_IP, ONOS_PORT, src_node))
            for port in port_reply['ports']:
                if port['port'] == src_port_number:
                    port_name = port['annotations']['portName']
                    bw = 50000
                    
                    lost = self.losses[port_name] if port_name in self.losses else 0 #MR
                    delayed = self.delay[port_name] if port_name in self.delay else 0 #MR
                    used = self.usage[port_name] if port_name in self.usage else 0
                    self.G.add_edge(src_node, dst_node, bandwidth=bw, used_bandwidth=used, loss=lost, delay=delayed)#MR
                #    print(port_name+' '+str(used))

            port_reply = json_get_req('http://%s:%d/onos/v1/devices/%s/ports' % (ONOS_IP, ONOS_PORT, dst_node))
            for port in port_reply['ports']:
                if port['port'] == dst_port_number:
                    port_name = port['annotations']['portName']
                    bw = 50000
                    used = self.usage[port_name] if port_name in self.usage else 0
                    lost = self.losses[port_name] if port_name in self.losses else 0 #MR
                    delayed = self.delay[port_name] if port_name in self.delay else 0 #MR
                    #print(bw)
                    #print(used)
                    #print("bwused")
                    self.G.add_edge(dst_node, src_node, bandwidth=bw, used_bandwidth=used, loss=lost, delay=delayed) #MR
                #    print(port_name+' '+str(used))


        reply = json_get_req('http://%s:%d/onos/v1/hosts' % (ONOS_IP, ONOS_PORT))
        if 'hosts' not in reply:
            return
        for host in reply['hosts']:
            self.G.add_node(host['id'], type='host')
            for location in host['locations']:
                self.G.add_edge(host['id'], location['elementId'], bandwidth= DEFAULT_ACCESS_CAPACITY, used_bandwidth=0, loss=0, delay=0) #MR
                self.G.add_edge(location['elementId'], host['id'], bandwidth= DEFAULT_ACCESS_CAPACITY, used_bandwidth=0, loss=0, delay=0) #MR
            self.hosts.append(host['id'])

        self.pos = nx.fruchterman_reingold_layout(self.G)

    def draw_topo(self, block=True):
        plt.figure()
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=self.hosts, node_shape='o', node_color='w')
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=self.devices, node_shape='s', node_color='b')
        nx.draw_networkx_labels(self.G.subgraph(self.hosts), self.pos, font_color='k')
        nx.draw_networkx_labels(self.G.subgraph(self.devices), self.pos, font_color='w',
                                labels=self.deviceId_to_chassisId)
        nx.draw_networkx_edges(self.G, self.pos)
        plt.show(block=block)
