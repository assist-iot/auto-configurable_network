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
    # h2 = net.addHost('h2', ip="10.0.1.2/24", mac="00:00:00:00:00:01", protocols="OpenFlow13")
    # h3 = net.addHost('h3', ip="10.0.1.3/24", mac="00:00:00:00:00:02", protocols="OpenFlow13")

    hosts = []
    for i in range(2, 10):
        host = net.addHost("h" + str(i), ip="10.0.1." + str(i) + "/24", mac="00:00:00:00:00:0" + str(i), protocols="OpenFlow13")
        hosts.append(host)
    for i in range(10, 15):
        host = net.addHost("h" + str(i), ip="10.0.1." + str(i) + "/24", mac="00:00:00:00:00:" + str(i), protocols="OpenFlow13")
        hosts.append(host)

    r1 = net.addHost('r1', ip="10.0.1.1/24", mac="00:00:00:00:00:01", protocols="OpenFlow13")
    # s1 = net.addSwitch('s1', protocols="OpenFlow13")
    # s2 = net.addSwitch('s2', protocols="OpenFlow13")

    switches = []
    for i in range(0, 8):
        switch = net.addSwitch("s" + str(i), protocols="OpenFlow13")
        switches.append(switch)

    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653, protocols="OpenFlow13")

    # net.addLink(r1, s1, bw=1)
    # net.addLink(h2, s1)
    # net.addLink(s1, s2)
    # net.addLink(h3, s2)

    # add links
    net.addLink(switches[0], r1, bw=1000)
    net.addLink(switches[0], switches[7], bw=100)
    net.addLink(hosts[12], switches[7], bw=100)
    for i in range(1, 6):
        print(switches[i])
        print(hosts[i * 2 - 1])
        print(hosts[i * 2])
        net.addLink(switches[i], hosts[i * 2 - 1], bw=1000)
        net.addLink(switches[i], hosts[i * 2], bw=1000)

    print("reszta")
    print(switches[6])
    print(hosts[0])
    print(hosts[11])
    # net.addLink(switches[4], hosts[9], bw=1000)     # ten i 10 - hosty zabrane z 5
    # net.addLink(switches[6], hosts[10], bw=1000)
    net.addLink(switches[6], hosts[0], bw=1000)
    net.addLink(switches[6], hosts[11], bw=1000)

    # for i in range(1, 4):
    #     net.addLink(switches[7], switches[i], bw=100, loss=1.5)
    # for i in range(4, 7):
    #     net.addLink(switches[7], switches[i], bw=100, loss=0)
    net.addLink(switches[7], switches[1], bw=40, loss=0)
    net.addLink(switches[7], switches[2], bw=40, loss=0)
    net.addLink(switches[7], switches[3], bw=40, loss=0)
    net.addLink(switches[7], switches[4], bw=40, loss=0)
    net.addLink(switches[7], switches[5], bw=40, loss=1)
    net.addLink(switches[7], switches[6], bw=40, loss=0)

    for i in range(1, 7):
        for j in range(i + 1, 7):
            net.addLink(switches[i], switches[j], bw=50)
            print(j)

    net.build()

    c0.start()
    # s1.start([c0])
    # s2.start([c0])
    for switch in switches:
        switch.start([c0])

    r1.cmd("ifconfig r1-enp0s3 0")  # ens?
    r1.cmd("ip addr add 10.0.1.1/24 brd + dev r1-enp0s3")
    r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    # h2.cmd("ip route add default via 10.0.1.1")
    # h3.cmd("ip route add default via 10.0.1.1")
    for host in hosts:
        host.cmd("ip route add default via 10.0.1.1")

    # Add physical interface
    print('Defining physical interface\n')
    intfName = 'enp0s8'  # enp
    print('Adding hardware interface', intfName, 'to router', r1.name, '\n')
    Intf(intfName, node=r1)

    # Add physical interface
    print('Defining physical interface\n')
    intfName = 'enp0s9'  # enp
    print('Adding hardware interface', intfName, 'to switch', switches[5].name, '\n')
    Intf(intfName, node=switches[0])

    r1.cmd("ip addr add 192.168.117.138/24 dev enp0s8")  # adres i enp
    r1.cmd("ip route add 192.168.117.0 via 192.168.117.138")  # adres
    # h2.cmd("ip route add 192.168.1.0 via 10.0.1.1")
    # h3.cmd("ip route add 192.168.1.0 via 10.0.1.1")
    for host in hosts:
        host.cmd("ip route add 192.168.1.0 via 10.0.1.1")

    sleep(10)
    r1.cmd('iperf -s &')
    # h2.cmd('iperf -c 10.0.1.1 -t 10 &')
    # h3.cmd('iperf -c 10.0.1.1 -t 10 &')
    for host in hosts:
        host.cmd('iperf -c 10.0.1.1 -t 10 &')
    print("po iperfach")
    sleep(30)
    r1.cmd(
        '/home/mich/Odzyskane/Desktop/topo4/NAPES 320 /home/mich/Odzyskane/Desktop/topo4/config_s.rcr '
        '/home/mich/Odzyskane/Desktop/topo4/logs/ >  /home/mich/Odzyskane/Desktop/topo4/logs/logs.txt &')
    # h2.cmd(
    #     '/home/mich/Odzyskane/Desktop/topo4/NAPES 320 /home/mich/Odzyskane/Desktop/topo4/config_c' + str(2) +
    #     '.rcr /home/mich/Odzyskane/Desktop/topo4/logs/ > /home/mich/Odzyskane/Desktop/topo4/logs/logc' + str(
    #         2) + '.txt &')
    # h3.cmd(
    #     '/home/mich/Odzyskane/Desktop/topo4/NAPES 320 /home/mich/Odzyskane/Desktop/topo4/config_c' + str(3) +
    #     '.rcr /home/mich/Odzyskane/Desktop/topo4/logs/ > /home/mich/Odzyskane/Desktop/topo4/logs/logc' + str(
    #         3) + '.txt &')

    for i in range(0, 12):
        hosts[i].cmd(
            '/home/mich/Odzyskane/Desktop/topo4/NAPES 320 /home/mich/Odzyskane/Desktop/topo4/config_c' + str(i+1) +
            '.rcr /home/mich/Odzyskane/Desktop/topo4/logs/ > /home/mich/Odzyskane/Desktop/topo4/logs/logc' + str(
                i+1) + '.txt &')

    # sleep(500)

    # delaye
    for i in range(1, 60):
        print("Testing network connectivity")
        net.pingFull(hosts=hosts, timeout=0.5)
        print("Testing network connectivity finished")
        sleep(2)

    print("*** Running CLI")
    CLI(net)

    print("*** Stopping network")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')

    topology()
