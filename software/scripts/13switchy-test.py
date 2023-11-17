from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from functools import partial
from mininet.node import OVSSwitch
from mininet.node import RemoteController
from time import sleep
from mininet.util import customClass
from mininet.link import TCLink
import subprocess


# Compile and run sFlow helper script
# - configures sFlow on OVS
# - posts topology to sFlow-RT
# execfile('sflow-rt/extras/sflow.py') - execfile wycofany z pythona3
# exec(open("/home/mich/sflow-rt/extras/sflow.py").read())


class MyTopo(Topo):

    def build(self):

        # add hosts and switches

        hosts = []
        for i in range(0, 13):
            host = self.addHost("h" + str(i))
            hosts.append(host)
        switches = []
        for i in range(0, 15):
            switch = self.addSwitch("sw" + str(i))
            switches.append(switch)

        # add links
        for i in range(1, 13):
            self.addLink(switches[i], hosts[i], bw=1000)

        for i in range(1, 13):
            self.addLink(switches[i], switches[13], bw=1000)

        self.addLink(switches[13], switches[14], bw=1000, loss=5)
        self.addLink(switches[13], switches[0], bw=1000, loss=30)
        self.addLink(switches[14], switches[0], bw=1000, loss=5)
        self.addLink(hosts[0], switches[0], bw=1000)

def test():
    topo = MyTopo()
    net = Mininet(topo=topo, controller=partial(RemoteController, ip='127.0.0.1', port=6653),
                  switch=partial(OVSSwitch, protocols='OpenFlow13'), link=TCLink)
    net.start()
    print("Net started")
    hosts = net.get('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12')
    h0 = net.get('h0')
    h0.cmd('iperf -s &')
    for host in hosts:
        host.cmd('iperf -c 10.0.0.1 -t 10 &')
    print("po iperfach")
    sleep(30)
    h0.cmd(
        '/home/mich/Odzyskane/Desktop/topo41/NAPES 320 /home/mich/Odzyskane/Desktop/topo41/config_s.rcr '
        '/home/mich/Odzyskane/Desktop/topo41/logs/ > /home/mich/Odzyskane/Desktop/topo41/logs/logs.txt &')
    for i in range(0, 12):
        hosts[i].cmd('/home/mich/Odzyskane/Desktop/topo41/NAPES 320 /home/mich/Odzyskane/Desktop/topo41/config_c' + str(
            i + 1) + '.rcr /home/mich/Odzyskane/Desktop/topo41/logs/ > /home/mich/Odzyskane/Desktop/topo41/logs/logc' + str(
            i + 1) + '.txt &')
        print(i)

    # for i in range(1, 100):
    #     print("Testing network connectivity")
    #     net.pingAllFull()
    #     sleep(2)

    sleep(500)
    net.stop()


if __name__ == '__main__':
    test()
