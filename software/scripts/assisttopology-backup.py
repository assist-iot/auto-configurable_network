from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink
from mininet.link import Intf
from mininet.topolib import TreeTopo
from time import sleep


def topology():
    net = Mininet(controller=RemoteController, link=TCLink, switch=OVSKernelSwitch)
    # Add hosts and switches
    h2 = net.addHost('h2', ip="10.0.1.2/24", mac="00:00:00:00:00:01", protocols="OpenFlow13")
    h3 = net.addHost('h3', ip="10.0.1.3/24", mac="00:00:00:00:00:02", protocols="OpenFlow13")
    r1 = net.addHost('r1', ip="10.0.1.1/24", mac="00:00:00:00:00:03", protocols="OpenFlow13")
    s1 = net.addSwitch('s1', protocols="OpenFlow13")
    s2 = net.addSwitch('s2', protocols="OpenFlow13")
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653, protocols="OpenFlow13")

    net.addLink(r1, s1, bw=1)
    net.addLink(h2, s1)
    net.addLink(s1, s2)
    net.addLink(h3, s2)

    net.build()

    c0.start()
    s1.start([c0])
    s2.start([c0])

    r1.cmd("ifconfig r1-eth0 0")  # ens?
    r1.cmd("ip addr add 10.0.1.1/24 brd + dev r1-eth0")
    r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    h2.cmd("ip route add default via 10.0.1.1")
    h3.cmd("ip route add default via 10.0.1.1")

    # Add physical interface
    print('Defining physical interface\n')
    intfName = 'enp0s8'  # enp
    print('Adding hardware interface', intfName, 'to router', r1.name, '\n')
    Intf(intfName, node=r1)

    # Add physical interface
    print('Defining physical interface\n')
    intfName = 'enp0s9'  # enp
    print('Adding hardware interface', intfName, 'to switch', s1.name, '\n')
    Intf(intfName, node=s1)

    r1.cmd("ip addr add 192.168.117.138/24 dev enp0s8")  # adres i enp
    r1.cmd("ip route add 192.168.117.0 via 192.168.117.138")  # adres
    h2.cmd("ip route add 192.168.1.0 via 10.0.1.1")
    h3.cmd("ip route add 192.168.1.0 via 10.0.1.1")

    # s1.cmd("ovs-ofctl add-flow s1 priority=1,arp,actions=flood")
    # s1.cmd("ovs-ofctl add-flow s1 priority=65535,ip,dl_dst=00:00:00:00:00:03,actions=output:1")
    # s1.cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.0.1.2,actions=output:2")
    #        s1.cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.0.1.3,actions=output:3")

    sleep(10)
    r1.cmd('iperf -s &')
    h2.cmd('iperf -c 10.0.1.1 -t 10 &')
    h3.cmd('iperf -c 10.0.1.1 -t 10 &')
    print("po iperfach")
    sleep(30)
    r1.cmd(
        '/home/mich/Odzyskane/Desktop/topo4/NAPES 320 /home/mich/Odzyskane/Desktop/topo4/config_s.rcr '
        '/home/mich/Odzyskane/Desktop/topo4/logs/ >  /home/mich/Odzyskane/Desktop/topo4/logs/logs.txt &')
    h2.cmd(
        '/home/mich/Odzyskane/Desktop/topo4/NAPES 320 /home/mich/Odzyskane/Desktop/topo4/config_c' + str(2) +
        '.rcr /home/mich/Odzyskane/Desktop/topo4/logs/ > /home/mich/Odzyskane/Desktop/topo4/logs/logc' + str(
            2) + '.txt &')
    h3.cmd(
        '/home/mich/Odzyskane/Desktop/topo4/NAPES 320 /home/mich/Odzyskane/Desktop/topo4/config_c' + str(3) +
        '.rcr /home/mich/Odzyskane/Desktop/topo4/logs/ > /home/mich/Odzyskane/Desktop/topo4/logs/logc' + str(
            3) + '.txt &')

    # sleep(500)

    print("*** Running CLI")
    CLI(net)

    print("*** Stopping network")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')

    topology()
