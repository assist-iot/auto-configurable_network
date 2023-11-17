from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink
from mininet.link import Intf
from mininet.topolib import TreeTopo


def topology():
    net = Mininet(controller=RemoteController, link=TCLink, switch=OVSKernelSwitch)
    # Add hosts and switches
    h2 = net.addHost('h2', ip="10.0.1.2/24", mac="00:00:00:00:00:01", protocols="OpenFlow13")
    h3 = net.addHost('h3', ip="10.0.1.3/24", mac="00:00:00:00:00:02", protocols="OpenFlow13")
    h4 = net.addHost('h4', ip="10.0.1.4/24", protocols="OpenFlow13")
    r1 = net.addHost('r1', ip="10.0.1.1/24", mac="00:00:00:00:00:03", protocols="OpenFlow13")
    s1 = net.addSwitch('s1', protocols="OpenFlow13")
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653, protocols="OpenFlow13")

    net.addLink(r1, s1, bw=1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s1)

    net.build()

    c0.start()
    s1.start([c0])

    r1.cmd("ifconfig r1-enp0s3 0")
    r1.cmd("ip addr add 10.0.1.1/24 brd + dev r1-enp0s3")
    r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    h2.cmd("ip route add default via 10.0.1.1")
    h3.cmd("ip route add default via 10.0.1.1")
    h4.cmd("ip route add default via 10.0.1.1")

    # Add physical interface
    print('Defining physical interface\n')
    intfName = 'enp0s8'
    print('Adding hardware interface', intfName, 'to router', r1.name, '\n')
    Intf(intfName, node=r1)

    # Add physical interface
    print('Defining physical interface\n')
    intfName = 'enp0s9'
    print('Adding hardware interface', intfName, 'to switch', s1.name, '\n')
    Intf(intfName, node=s1)

    r1.cmd("ip addr add 192.168.1.44/24 dev enp0s8")
    r1.cmd("ip route add 192.168.1.0 via 192.168.1.44")
    h2.cmd("ip route add 192.168.1.0 via 10.0.1.1")
    h3.cmd("ip route add 192.168.1.0 via 10.0.1.1")

    s1.cmd("ovs-ofctl add-flow s1 priority=1,arp,actions=flood")
    s1.cmd("ovs-ofctl add-flow s1 priority=65535,ip,dl_dst=00:00:00:00:00:03,actions=output:1")
    s1.cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.0.1.2,actions=output:2")
    s1.cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.0.1.3,actions=output:3")
    s1.cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.0.1.4,actions=output:4")

    print("*** Running CLI")

    CLI(net)

    print("*** Stopping network")

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')

    topology()
