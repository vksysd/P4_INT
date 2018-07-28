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
from collections import deque
from collections import defaultdict
import commands
HOPS = 4
ShimSize = 4
TailSize = 4
INTSize = 8
METADATA_FIELDS_CAPTURED = 3
MetadataSize = 12
TOTAL_SIZE_FOR_EACH_FIELD = 16;  # = no of switches * collected field size from each switch
total_packets_recvd = 0
experiment_starts = datetime.now()
next_port = 3
q = deque()
time_elapsed = 0.1 # initial sliding window frame = 1 second
update_flag = 0
l = [] #empty list to store (hash,udpsrcport) in list on tuples
port_identified = 0
last_port_identified = 0
packet_len_sum = 0
AVG_PACKET_LENGTH_THRESHHOLD = 1000
QDEPTH_THRESHHOLD = 50
next_port_list = []

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


def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

def handle_pkt(pkt):
    #open file for writing results
    global experiment_starts
    global total_packets_recvd
    global time_elapsed
    global update_flag
    global l
    global port_identified
    global last_port_identified
    global packet_len_sum
    global next_port
    if total_packets_recvd == 0:
        experiment_starts = datetime.now()

    dirpath = os.getcwd()
    #print("current directory is : " + dirpath)
    foldername = os.path.basename(dirpath)
    #print("Directory name is : " + foldername)
    rfile = open(dirpath+"/INT_udp_flows_results_from_h1.txt","a")
    #print("got a packet")
    #print("pkt length=")
    #print(len(pkt))
    # pkt.show2()
    #print "IP src =" ,
    #print pkt[IP].src

    #print "IP dst =" ,
    #print pkt[IP].dst

    total_packets_recvd = total_packets_recvd + 1;
    time_now = datetime.now()
    time_to_write = (time_now - experiment_starts).total_seconds()
    p1 = pkt.copy()

    p1 = p1.payload.payload.payload
    if(sys.argv[1]=="10.0.2.15"):
        p1_bytes = bytes(p1)

        # ShimHeader(p1_bytes[0:ShimSize]).show()
        p1_bytes = p1_bytes[ShimSize:]

        x = INTHeader(p1_bytes[0:INTSize])
        # print(" int.rsvd3 =",x.rsvd3)
        # INTHeader(p1_bytes[0:INTSize]).show()
        p1_bytes = p1_bytes[INTSize:]
        rfile.write(str(time_to_write))
        rfile.write(",")
        rfile.write(str(pkt[IP].src))
        rfile.write(",")
        rfile.write(str(pkt[IP].dst))
        rfile.write(",")
        rfile.write(str(pkt[UDP].sport))
        rfile.write(",")
        rfile.write(str(pkt[UDP].dport))
        rfile.write(",")
        rfile.write(str(x.rsvd3))
        rfile.write(",")
        rfile.write(str(pkt[IP].len))
        rfile.write(",")
        
        # print("time_elapsed = ",time_elapsed)
        compare = (time_now - experiment_starts).total_seconds()
        # print("compare = ",compare)
        
        if ((time_now - experiment_starts).total_seconds() < time_elapsed) :
            # add elements to the array
            l.append((x.rsvd3,pkt[UDP].sport,pkt[IP].len))
            # print ("inside if")
            # print("l=",l)
        # write logic for finding max occuring element from list
        elif len(l) > 0 :
            # print("inside else")
            time_in_elif = datetime.now()
            #find the max repeated element from list
            d = defaultdict(int)
            for i in [i[0] for i in l]:
                d[i] += 1
            result = max(d.items(), key=lambda x: x[1])
            # print ("result = ",result)
            # print(" max repeated element in list = ",result[0]) # max repeated element in list
            # print("count of max repeated element = ",result[1]) #count of element
            # print("length of list in 1 sec = ",len(l))
            packet_len_index_to_sum = list_duplicates_of([i[0] for i in l],result[0])
            # print("external function returns = ",packet_len_index_to_sum)
            for i in packet_len_index_to_sum:
                # print("packet length at", i,"=",l[i][2])
                packet_len_sum += l[i][2]
            # print("length packet_len_index_to_sum = ",len(packet_len_index_to_sum))
            average_packet_length_of_identified_flow = packet_len_sum/len(packet_len_index_to_sum)
            # print("average_packet_length_of_identified_flow = ",average_packet_length_of_identified_flow)
            if (result[1] > len(l)/4): # if the count of max repeating element exceeds 1/3rd of the len(list) we assume it is a heavy flow
                index_found = [i[0] for i in l].index(result[0])
                # print("index found = ",index_found)
                # print("port found = ", l[index_found][1])
                # print("len of the found packet = ",l[index_found][2])
                # if the average packet length of the identified flow exceeds AVG_PACKET_LENGTH_THRESHHOLD then modify the route
                if average_packet_length_of_identified_flow > AVG_PACKET_LENGTH_THRESHHOLD :
                    port_identified = l[index_found][1]
                    # print ("port_identified = ",port_identified)
                    # print(" last_port_identified = ",last_port_identified)
                    if last_port_identified != port_identified :
                        update_flag = 1 # triger to modify field if the threshold on the bottleneck switch crosses
                        print("update_flag = ",update_flag)
                
                    # update_flag = 1
                    del l[:]
                    packet_len_sum = 0
                    # print("l after reinitialization = ", l)
            time_elapsed += 0.1 # increment the sliding window by 1 second
            time_elapsed += (datetime.now()-time_in_elif).total_seconds()
            # print("updated time_elapsed in elif = ",time_elapsed)


        else : 
            print("timeout")
            time_elapsed += 0.1 # increment the sliding window by 1 second
        
        print_qdepth_flag = 0
        for i in range(METADATA_FIELDS_CAPTURED):
            if i == 0:
                p2 = MetadataHeader_switchid(p1_bytes[0:TOTAL_SIZE_FOR_EACH_FIELD])
            if i == 1:
                p2 = MetadataHeader_hoplatency(p1_bytes[0:TOTAL_SIZE_FOR_EACH_FIELD])
            if i ==2:
                p2 = MetadataHeader_qdepth(p1_bytes[0:TOTAL_SIZE_FOR_EACH_FIELD])

            #p2.show()
            
            if i == 0 :
                # print "SwitchID1 = ", p2.SwitchID1
                rfile.write(str(p2.SwitchID1))
                rfile.write(",")
                # print "SwitchID2 = ", p2.SwitchID2
                rfile.write(str(p2.SwitchID2))
                rfile.write(",")
                # print "SwitchID3 = ", p2.SwitchID3
                rfile.write(str(p2.SwitchID3))
                rfile.write(",")
                # print "SwitchID4 = ", p2.SwitchID4
                rfile.write(str(p2.SwitchID4))
                rfile.write(",")
                if p2.SwitchID2 == 3:
                    print_qdepth_flag = 1
            if i == 1 :
                # print "hop_latency1 = ", p2.Hop_Latency1
                rfile.write(str(p2.Hop_Latency1))
                rfile.write(",")
                # print "hop_latency2 = ", p2.Hop_Latency2
                rfile.write(str(p2.Hop_Latency2))
                rfile.write(",")
                # print "hop_latency3 = ", p2.Hop_Latency3
                rfile.write(str(p2.Hop_Latency3))
                rfile.write(",")
                # print "hop_latency4 = ", p2.Hop_Latency4
                rfile.write(str(p2.Hop_Latency4))
                rfile.write(",")
            if i == 2 :
                # print "qid1 = ", p2.qid1
                # rfile.write(str(p2.qid1))
                # rfile.write(" ")
                # print "qdepth1 = ", p2.qdepth1
                rfile.write(str(p2.qdepth1))
                rfile.write(",")
                # print "qid2 = ", p2.qid2
                # rfile.write(str(p2.qid2))
                # rfile.write(" ")
                

                rfile.write(str(p2.qdepth2))
                rfile.write(",")
                if print_qdepth_flag:
                    if p2.qdepth2 > 0 :
                        print "qdepth at switch S3 = ", p2.qdepth2
                        pass
                    print_qdepth_flag = 0
                    if (int(p2.qdepth2) > QDEPTH_THRESHHOLD) & update_flag == 1 :
                        time_in_update_entry = datetime.now()
                        update_flag = 0
                        get_entry_num = str("echo table_dump_entry_from_key ipv4_lpm "+str(pkt[IP].src)+" "+str(pkt[IP].dst)+"/32 "+str(port_identified)+" "+str(pkt[UDP].dport)+" | simple_switch_CLI --thrift-port 9091 | grep 'Dumping entry' | awk '{print $4}'")
                        # print("get_entry_num = ",get_entry_num)

                        z = commands.getstatusoutput(get_entry_num)
                        print("z = ",z)
                        i = z[1].split("x")[1]
                        entry_num = int(i, 16)
                        # entry_num = 2*(port_identified-7000)+1
                        last_port_identified = port_identified
                        # print("entry num = ", entry_num)
                        # next_port = 3
                        next_port_list.append(next_port)
                        command_to_run = "echo table_modify ipv4_lpm ipv4_forward "+str(entry_num)+" "+str(pkt[Ether].dst)+" "+str(next_port)+" | simple_switch_CLI --thrift-port 9091"
                        # print("command_to_run = ",command_to_run)
                        y = commands.getstatusoutput(command_to_run)
                        next_port += 1
                        if next_port > 5:
                            next_port = 3
                        # print("status output = ",y) 
                        # print("next_port = ",next_port)
                        time_elapsed += (datetime.now()-time_in_update_entry).total_seconds()
                        # if len(next_port_list) > 20 :
                            # print(next_port_list)
                            # exit(0)
                    # print("updated time_elapsed in for loop = ",time_elapsed)
                # print "qid3 = ", p2.qid3
                # rfile.write(str(p2.qid3))
                # rfile.write(" ")
                # print "qdepth3 = ", p2.qdepth3
                rfile.write(str(p2.qdepth3))
                rfile.write(",")
                # print "qid4 = ", p2.qid4
                # rfile.write(str(p2.qid4))
                # rfile.write(" ")
                # print "qdepth4 = ", p2.qdepth4
                rfile.write(str(p2.qdepth4))
                # rfile.write(" ")
            p1_bytes = p1_bytes[TOTAL_SIZE_FOR_EACH_FIELD:]

        rfile.write("\n")
        if time_to_write > 180 :
            print("total_packets_recvd = ",total_packets_recvd)
            # pass

        # TailHeader(p1_bytes).show()

        # hexdump(pkt)
        sys.stdout.flush()
        rfile.close()
    else :
        pass
         # print("total_packets_recvd = ",total_packets_recvd)

def main():
    #total_packets_recvd=0;
    ifaces = filter(lambda i: 'eth' in i, os.listdir('/sys/class/net/'))
    iface = ifaces[0]
    print("sniffing on %s" % iface)
    sys.stdout.flush()
    #print ("before sniff")
    sniff(filter="udp and host 10.0.1.1 and dst port 8080", iface = iface,
          prn = lambda x: handle_pkt(x))
    #print("total_packets_recvd = ",total_packets_recvd)
if __name__ == '__main__':
    main()
