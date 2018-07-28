#!/usr/bin/env python
#sends random number of packets to the sink host
import argparse
import sys
import socket
import random
import struct

from scapy.all import sendp, send, get_if_list, get_if_hwaddr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP

def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface

def main():

    if len(sys.argv)<3:
        print('pass 2 arguments: <destination> "<message>"')
        exit(1)

    addr = socket.gethostbyname(sys.argv[1])
    iface = get_if()

    print("sending on interface %s to %s" % (iface, str(addr)))
    total_pkts = 0
    random_ports = random.sample(xrange(1024, 65535), 10)
    for port in random_ports:
        num_packets = random.randint(1, 2)
        for i in range(num_packets):
            #data = randomword(100)
            pkt =  Ether(src=get_if_hwaddr(iface), dst='00:00:00:00:01:01')
            #pkt = pkt /IP(dst=addr) / UDP() / sys.argv[2]
            pkt = pkt /IP(dst=addr) / TCP(dport=port, sport=random.randint(49152,65535)) / sys.argv[2]
            pkt.show2()
            sendp(pkt, iface=iface, verbose=False)
            total_pkts += 1
    print "Sent %s packets in total" % total_pkts

if __name__ == '__main__':
    main()
