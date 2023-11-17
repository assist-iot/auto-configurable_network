from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from functools import partial
from mininet.node import OVSSwitch
from mininet.node import RemoteController
from mininet.log import setLogLevel
from time import sleep


class MyTopo(Topo):

    def build(self):

        # add hosts and switches

        hosts = []
        for i in range(0, 13):
            host = self.addHost("h" + str(i))
            hosts.append(host)
        switches = []
        for i in range(0, 13):
            switch = self.addSwitch("sw" + str(i))
            switches.append(switch)

        # add links
        for i in range(0, 13):
            self.addLink(switches[i], hosts[i], bw=1000)

        self.addLink(switches[0], switches[1], bw=50, loss=10)
        for i in range(1, 10):
            self.addLink(switches[i], switches[i + 1], bw=50)

        self.addLink(switches[9], switches[0], bw=50, loss=10)
        self.addLink(switches[10], switches[11], bw=50)
        self.addLink(switches[10], switches[0], bw=50, loss=15)
        self.addLink(switches[10], switches[8], bw=50)
        self.addLink(switches[10], switches[9], bw=50)
        self.addLink(switches[11], switches[6], bw=50)
        self.addLink(switches[12], switches[0], bw=50, loss=20)
        self.addLink(switches[3], switches[0], bw=50, loss=20
                     )
        self.addLink(switches[12], switches[4], bw=50)
        self.addLink(switches[12], switches[5], bw=50)


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

    for i in range(1, 60):
        print("Testing network connectivity")
        net.pingFull(hosts=hosts, timeout=0.5)
        sleep(2)

    sleep(180)

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    test()
