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
# import server

HOPS = 4
ShimSize = 4
TailSize = 4
INTSize = 8
METADATA_FIELDS_CAPTURED = 3
MetadataSize = 12
TOTAL_SIZE_FOR_EACH_FIELD = 16;  # = no of switches * collected field size from each switch
total_packets_recvd = 0
experiment_starts = datetime.now()

if len(sys.argv) < 2:
    print "./receive_tcp_multithreaded.py <host ip>"
    exit(0)

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


class MetadataHeader_switchid(Packet):
    name = 'Metadata switch id Header'
    fields_desc = [
        IntField('SwitchID1', 0),
        IntField('SwitchID2', 0),
        IntField('SwitchID3', 0),
        IntField('SwitchID4', 0)
    ]
class MetadataHeader_hoplatency(Packet):
    name = 'Metadata hop latency Header'
    fields_desc = [
        IntField('Hop_Latency1', 0),
        IntField('Hop_Latency2', 0),
        IntField('Hop_Latency3', 0),
        IntField('Hop_Latency4', 0)
    ]
class MetadataHeader_qdepth(Packet):
    name = 'Metadata qdepth Header'
    fields_desc = [
        ByteField('qid1', 0),
        BitField('qdepth1', 0, 24),
        ByteField('qid2', 0),
        BitField('qdepth2', 0, 24),
        ByteField('qid3', 0),
        BitField('qdepth3', 0, 24),
        ByteField('qid4', 0),
        BitField('qdepth4', 0, 24)
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
    rfile = open(dirpath+"/INT_tcp_flows_results.txt","a")
    #print("got a packet")
    #print("pkt length=")
    #print(len(pkt))
    # pkt.show2()
    pkt.show()
    #print "IP src =" ,
    #print pkt[IP].src

    #print "IP dst =" ,
    #print pkt[IP].dst
    total_packets_recvd = total_packets_recvd + 1;

    time_now = datetime.now()
    time_to_write = (time_now - experiment_starts).total_seconds()
    p1 = pkt.copy()

    p1 = p1.payload.payload.payload
    # p1.show2()
    p1.show()
    if(sys.argv[1]=="10.0.2.15"):
        p1_bytes = bytes(p1)
        # ShimHeader(p1_bytes[0:ShimSize]).show()
        # p1_bytes = p1_bytes[ShimSize:]

        # INTHeader(p1_bytes[0:INTSize]).show()
        # p1_bytes = p1_bytes[INTSize:]

        for i in range(METADATA_FIELDS_CAPTURED):
            if i == 0:
                p2 = MetadataHeader_switchid(p1_bytes[0:TOTAL_SIZE_FOR_EACH_FIELD])
            if i == 1:
                p2 = MetadataHeader_hoplatency(p1_bytes[0:TOTAL_SIZE_FOR_EACH_FIELD])
            if i ==2:
                p2 = MetadataHeader_qdepth(p1_bytes[0:TOTAL_SIZE_FOR_EACH_FIELD])

            p2.show()
            rfile.write(str(time_to_write))
            rfile.write(" ")
            rfile.write(str(pkt[IP].src))
            rfile.write(" ")
            rfile.write(str(pkt[IP].dst))
            rfile.write(" ")
            if i == 0 :
                # print "SwitchID1 = ", p2.SwitchID1
                rfile.write(str(p2.SwitchID1))
                rfile.write(" ")
                # print "SwitchID2 = ", p2.SwitchID2
                rfile.write(str(p2.SwitchID2))
                rfile.write(" ")
                # print "SwitchID3 = ", p2.SwitchID3
                rfile.write(str(p2.SwitchID3))
                rfile.write(" ")
                # print "SwitchID4 = ", p2.SwitchID4
                rfile.write(str(p2.SwitchID4))
                rfile.write(" ")
            if i == 1 :
                #print "hop_latency1 = ", p2.Hop_Latency1
                rfile.write(str(p2.Hop_Latency1))
                rfile.write(" ")
                #print "hop_latency2 = ", p2.Hop_Latency2
                rfile.write(str(p2.Hop_Latency2))
                rfile.write(" ")
                #print "hop_latency3 = ", p2.Hop_Latency3
                rfile.write(str(p2.Hop_Latency3))
                rfile.write(" ")
                #print "hop_latency4 = ", p2.Hop_Latency4
                rfile.write(str(p2.Hop_Latency4))
                rfile.write(" ")
            if i == 2 :
                #print "qid1 = ", p2.qid1
                rfile.write(str(p2.qid1))
                rfile.write(" ")
                #print "qdepth1 = ", p2.qdepth1
                rfile.write(str(p2.qdepth1))
                rfile.write(" ")
                #print "qid2 = ", p2.qid2
                rfile.write(str(p2.qid2))
                rfile.write(" ")
                #print "qdepth2 = ", p2.qdepth2
                rfile.write(str(p2.qdepth2))
                rfile.write(" ")
                #print "qid3 = ", p2.qid3
                rfile.write(str(p2.qid3))
                rfile.write(" ")
                #print "qdepth3 = ", p2.qdepth3
                rfile.write(str(p2.qdepth3))
                rfile.write(" ")
                #print "qid4 = ", p2.qid4
                rfile.write(str(p2.qid4))
                rfile.write(" ")
                #print "qdepth4 = ", p2.qdepth4
                rfile.write(str(p2.qdepth4))
                rfile.write(" ")
            rfile.write("\n")
            p1_bytes = p1_bytes[TOTAL_SIZE_FOR_EACH_FIELD:]


         
        print("total_packets_recvd = ",total_packets_recvd)
        # ShimHeader(p1_bytes[0:ShimSize]).show()
        # p1_bytes = p1_bytes[ShimSize:]

        # INTHeader(p1_bytes[0:INTSize]).show()
        # p1_bytes = p1_bytes[INTSize:]
        TailHeader(p1_bytes).show()

        #hexdump(pkt)
        sys.stdout.flush()
        rfile.close()

    else :
         print("total_packets_recvd = ",total_packets_recvd)


def main():
    #total_packets_recvd=0;
    #os.system('python3 -m http.server 8080');
    ifaces = filter(lambda i: 'eth' in i, os.listdir('/sys/class/net/'))
    iface = ifaces[0]
    print("sniffing on %s" % iface)
    sys.stdout.flush()
    #print ("before sniff")
    sniff(filter="tcp and host 10.0.1.1 and dst port 8080", iface = iface,
          prn = lambda x: handle_pkt(x))
    #print("total_packets_recvd = ",total_packets_recvd)
if __name__ == '__main__':
    main()
