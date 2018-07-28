#!/usr/bin/env python
# attempt to parse switch id, ingress & egress ports, hop latency, qid & qdepth
import sys
import struct
import os
from datetime import datetime

from scapy.all import sniff, sendp, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import ShortField, IntField, LongField, BitField, FieldListField, FieldLenField, ByteField
from scapy.all import Ether, IP, UDP, TCP, Raw
from scapy.layers.inet import _IPOption_HDR

HOPS = 4
ShimSize = 4
TailSize = 4
INTSize = 8
MetadataSize = 12
total_packets_recvd = 0
experiment_starts = datetime.now()

class ShimHeader(Packet):
    name = 'Shim Header'
    fields_desc = [
        ByteField('int_type', 0),
        ByteField('rsvd1', 0),
        ByteField('len', 0),
        ByteField('rsvd2', 0),
    ]


class TailHeader(Packet):
    name = 'Tail Header'
    fields_desc = [
        ByteField('next_proto', 0),
        ShortField('dest_port', 0),
        ByteField('dscp', 0),
    ]


class INTHeader(Packet):
    name = 'INT Header'
    fields_desc = [
        BitField('ver', 0, 4),
        BitField('rep', 0, 2),
        BitField('c', 0, 1),
        BitField('e', 0, 1),
        BitField('m', 0, 1),
        BitField('rsvd1', 0, 7),
        BitField('rsvd2', 0, 3),
        BitField('ins_cnt', 0, 5),
        ByteField('remaining_hop_cnt', 0),
        BitField('instruction_mask_0003', 0, 4),
        BitField('instruction_mask_0407', 0, 4),
        BitField('instruction_mask_0811', 0, 4),
        BitField('instruction_mask_1215', 0, 4),
        ShortField('rsvd3', 0)
    ]


class MetadataHeader(Packet):
    name = 'Metadata Header'
    fields_desc = [
        IntField('SwitchID', 0),
        #ShortField('IngressPort', 0),
        #ShortField('EgressPort', 0), # ShortField means 16 bytes
        IntField('Hop_Latency', 0),
        ByteField('qid', 0),
        BitField('qdepth', 0, 24)
    ]


def get_if():
    ifs=get_if_list()
    iface=None
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface

class IPOption_MRI(IPOption):
    name = "MRI"
    option = 31
    fields_desc = [ _IPOption_HDR,
                    FieldLenField("length", None, fmt="B",
                                  length_of="swids",
                                  adjust=lambda pkt,l:l+4),
                    ShortField("count", 0),
                    FieldListField("swids",
                                   [],
                                   IntField("", 0),
                                   length_from=lambda pkt:pkt.count*4) ]


def handle_pkt(pkt):
    #open file for writing results
    global experiment_starts
    global total_packets_recvd
    if total_packets_recvd == 0:
        experiment_starts = datetime.now()

    dirpath = os.getcwd()
    #print("current directory is : " + dirpath)
    foldername = os.path.basename(dirpath)
    #print("Directory name is : " + foldername)
    rfile = open(dirpath+"/../INT_udp_results.txt","a")
    #print("got a packet")
    #print("pkt length=")
    #print(len(pkt))
    pkt.show2()
    #print "IP src =" ,
    #print pkt[IP].src

    #print "IP dst =" ,
    #print pkt[IP].dst
    total_packets_recvd = total_packets_recvd + 1;

    time_now = datetime.now()
    time_to_write = (time_now - experiment_starts).total_seconds()
    p1 = pkt.copy()

    p1 = p1.payload.payload.payload

    p1_bytes = bytes(p1)

    #ShimHeader(p1_bytes[0:ShimSize]).show()
    p1_bytes = p1_bytes[ShimSize:]

    #INTHeader(p1_bytes[0:INTSize]).show()
    p1_bytes = p1_bytes[INTSize:]

    for i in range(HOPS):
        p2 = MetadataHeader(p1_bytes[0:MetadataSize])
        #p2.show()
        rfile.write(str(time_to_write))
        rfile.write(" ")

        rfile.write(str(pkt[IP].src))
        rfile.write(" ")
        rfile.write(str(pkt[IP].dst))
        rfile.write(" ")
        #print "SwitchID = ", p2.SwitchID
        rfile.write(str(p2.SwitchID))
        rfile.write(" ")
        #print "IngressPort = ", p2.IngressPort
        #rfile.write(str(p2.IngressPort))
        #rfile.write(" ")
        #print "EgressPort = ", p2.EgressPort
        #rfile.write(str(p2.EgressPort))
        #rfile.write(" ")
        #print "hop_latency = ", p2.Hop_Latency
        rfile.write(str(p2.Hop_Latency))
        rfile.write(" ")
        #print "qid = ", p2.qid
        rfile.write(str(p2.qid))
        rfile.write(" ")
        #print "qdepth = ", p2.qdepth
        rfile.write(str(p2.qdepth))
        rfile.write("\n")

        p1_bytes = p1_bytes[MetadataSize:]
    print("total_packets_recvd = ",total_packets_recvd)

    #TailHeader(p1_bytes).show()

#    hexdump(pkt)
    sys.stdout.flush()
    rfile.close()


def main():
    #total_packets_recvd=0;
    ifaces = filter(lambda i: 'eth' in i, os.listdir('/sys/class/net/'))
    iface = ifaces[0]
    print("sniffing on %s" % iface)
    sys.stdout.flush()
    #print ("before sniff")
    sniff(filter="udp and ip", iface = iface,
          prn = lambda x: handle_pkt(x))
    #print("total_packets_recvd = ",total_packets_recvd)
if __name__ == '__main__':
    main()
