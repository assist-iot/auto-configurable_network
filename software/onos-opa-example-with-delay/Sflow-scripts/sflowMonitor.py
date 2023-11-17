#!/bin/env python
from mininet.net import Mininet
from mininet.util import quietRun
from requests import put
from os import listdir, environ
import re
import socket
import fcntl
import array
import struct
import os
import sys
import json

collector = environ.get('COLLECTOR', '127.0.0.1')
sampling = environ.get('SAMPLING', '10')
polling = environ.get('POLLING', '10')

switchlist = []
result = os.popen("sudo ovs-vsctl list-br").read()
data = result.split('\n')
for i in range(len(data) - 1):
    switchlist.append(data[i])


def getIfInfo(dst):
    is_64bits = sys.maxsize > 2 ** 32
    struct_size = 40 if is_64bits else 32
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    max_possible = 8  # initial value
    while True:
        bytes = max_possible * struct_size
        names = array.array('B')
        for i in range(0, bytes):
            names.append(0)
        outbytes = struct.unpack('iL', fcntl.ioctl(
            s.fileno(),
            0x8912,  # SIOCGIFCONF
            struct.pack('iL', bytes, names.buffer_info()[0])
        ))[0]
        if outbytes == bytes:
            max_possible *= 2
        else:
            break
    try:
        namestr = names.tobytes()
        namestr = namestr.decode('utf-8')
    except AttributeError:
        namestr = names.tostring()
    s.connect((dst, 0))
    ip = s.getsockname()[0]
    for i in range(0, outbytes, struct_size):
        name = namestr[i:i + 16].split('\0', 1)[0]
        addr = socket.inet_ntoa(namestr[i + 20:i + 24].encode('utf-8'))
        if addr == ip:
            return (name, addr)


(ifname, agent) = getIfInfo(collector)


def configSFlow(switchlist, collector, ifname, sampling, polling):
    print("*** Enabling sFlow:")
    sflow = 'sudo ovs-vsctl -- --id=@sflow create sflow agent=%s target=%s sampling=%s polling=%s --' % (
    ifname, collector, sampling, polling)
    for s in switchlist:
        sflow += ' -- set bridge %s sflow=@sflow' % s
        print("sflow %s is here" % s)
        k = os.popen(sflow).read()
        print(k)
        print(ifname)


configSFlow(switchlist, collector, ifname, sampling, polling)


def sendTopology(switchlist, agent, collector):
    print("*** Sending topology")
    topo = {'nodes': {}, 'links': {}}
    for s in switchlist:
        topo['nodes'][s] = {'agent': agent, 'ports': {}}
    path = '/sys/devices/virtual/net/'
    print(path)
    for child in listdir(path):
        print(child)
        parts = re.match('(^.+)-(.+)', child)
        if parts == None: continue
        if parts.group(1) in topo['nodes']:
            ifindex = open(path + child + '/ifindex').read().split('\n', 1)[0]
            topo['nodes'][parts.group(1)]['ports'][child] = {'ifindex': ifindex}

    reqID = os.popen("curl -u onos:rocks -X GET http://localhost:8181/onos/v1/devices | jq '.'").read()
    data2 = json.loads(reqID)
    devices = data2['devices']
    IDlist = []
    for device in devices:
        id = device['id']
        IDlist.append(id)
    result = os.popen("curl -u onos:rocks -X GET http://localhost:8181/onos/v1/links | jq '.'").read()
    data = json.loads(result)
    Links = data["links"]
    intfss = []
    for link in Links:

        i = 0
        for s1 in IDlist:
            j = 0
            for s2 in IDlist:
                if j > i:
                    if s1 == link['src']['device']:
                        ports = link['src']['port']
                        if s2 == link['dst']['dvice']:
                            portd = link['dst']['device']
                            ss = 's1' + '/' + ports
                            sd = 's2' + '/' + portd
                            intfs = []
                            intfs.append(ss)
                            intfs.append(sd)
                            intfss.append(intfs)

                for intf in intfss:
                    s1ifIdx = topo['nodes'][s1]['ports'][intf[0]]['ifindex']
                    s2ifIdx = topo['nodes'][s2]['ports'][intf[1]]['ifindex']
                    linkName = '%s-%s' % (s1, s2)
                    topo['links'][linkName] = {'node1': s1, 'port1': intf[0], 'node2': s2, 'port2': intf[1]}
            j += 1
        i += 1

    put('http://localhost:8008/topology/json', json=topo)

# sendTopology(switchlist,agent,collector)
