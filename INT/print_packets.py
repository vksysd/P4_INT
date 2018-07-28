from scapy.all import rdpcap

# Read all the packets from a pcap file in the form of a list
packets = rdpcap('s3-eth1_in.pcap')

# Go over all packets
for packet in packets:
    # Checking for presence of UDP layer
    if packet.haslayer('TCP'):
        # Pretty print packet showing values of all attributes in all layers
        packet.show()
