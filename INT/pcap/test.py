from scapy.all import rdpcap, Packet
from scapy.all import IntField, ShortField, ByteField, BitField

packets = rdpcap('s2-eth2_in.pcap')

HOPS = 2
ShimSize = 4
TailSize = 4
INTSize = 8
MetadataSize = 16


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
        ShortField('IngressPort', 0),
        ShortField('EgressPort', 0),  # ShortField means 16 bytes
        IntField('Hop_Latency', 0),
        ByteField('Qid', 0),
        BitField('Qdepth', 0, 24)
    ]


p1 = packets[0].copy()

p1 = p1.payload.payload.payload

p1_bytes = bytes(p1)

ShimHeader(p1_bytes[0:ShimSize]).show()
p1_bytes = p1_bytes[ShimSize:]

INTHeader(p1_bytes[0:INTSize]).show()
p1_bytes = p1_bytes[INTSize:]

for i in range(HOPS):
    p2 = MetadataHeader(p1_bytes[0:MetadataSize])
    p2.show()
    print(p2.SwitchID)
    print(p2.Hop_Latency)
    p1_bytes = p1_bytes[MetadataSize:]

TailHeader(p1_bytes).show()
