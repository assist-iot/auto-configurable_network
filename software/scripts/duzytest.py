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

        #add hosts and switches

        hosts=[]
        for i in range(0,13):
            host = self.addHost("h"+str(i))
            hosts.append(host)
        switches=[]
        for i in range(0,10):
            switch = self.addSwitch("sw"+str(i))
            switches.append(switch)

        #add links

        self.addLink(hosts[0], switches[0], bw=1000)
        for i in range(1,4):
            self.addLink(switches[0], switches[i], bw = 50, loss=3, max_queue_size=10)
            self.addLink(switches[i], switches[i*2+2], bw = 50, loss=3, max_queue_size=10)
            self.addLink(switches[i], switches[i*2+3], bw = 50, loss=3, max_queue_size=10)
        for i in range(1,3):
            self.addLink(switches[i], switches[i+1], bw = 50, max_queue_size = 10)
        for i in range(4,9):
            self.addLink(switches[i], switches[i+1], bw = 50, max_queue_size=10)
        for i in range(4,10):
            self.addLink(switches[i], hosts[i*2-7],bw = 1000, loss=3)
            self.addLink(switches[i], hosts[i*2-6], bw = 1000, loss=3)

def test():
    topo = MyTopo()
    net = Mininet( topo = topo, controller=partial( RemoteController, ip='127.0.0.1', port = 6653 ), switch = partial(OVSSwitch, protocols = 'OpenFlow13'), link = TCLink)
    net.start()
    print("Net started")
    hosts = net.get('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12')
    h0 = net.get('h0')
    h0.cmd('iperf -s &')
    for host in hosts:
        host.cmd('iperf -c 10.0.0.1 -t 10 &')
    print("po iperfach")
    sleep(30)
    h0.cmd('/home/mr/Praca/lab/topo41/NAPES 320 /home/mr/Praca/lab/topo41/config_s.rcr /home/mr/Praca/lab/topo41/logs/ > /home/mr/Praca/lab/topo41/logs/logs.txt &')
    for i in range(0,12):
        hosts[i].cmd('/home/mr/Praca/lab/topo41/NAPES 320 /home/mr/Praca/lab/topo41/config_c' + str(i) + '.rcr /home/mr/Praca/lab/topo41/logs/ > /home/mr/Praca/lab/topo41/logs/logc' + str(i) +'.txt &')
        print(i)

    for i in range(1, 100):
        print("Testing network connectivity")
        net.pingAllFull()

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    test()
