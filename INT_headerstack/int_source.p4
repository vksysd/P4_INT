/********************************************************************
* int_source.p4: tables, actions, and control flow
*******************************************************************/
#include <core.p4>
#include <v1model.p4>
#include "includes/headers.p4"
#include "includes/parser.p4"
#include "includes/int_definitions.p4"
#include "includes/checksums.p4"
#include "int_transit_source_common.p4"



// Insert INT header to the packet
control process_int_source_headers (inout headers hdr,inout metadata meta,inout standard_metadata_t standard_metadata) {

    action int_source(bit<5> ins_cnt, bit<4> ins_mask0003,bit<4> ins_mask0407) {
        // insert INT shim header
        hdr.intl4_shim.setValid();
        // int_type: Hop-by-hop type (1) , destination type (2)
        hdr.intl4_shim.int_type = 1;
        hdr.intl4_shim.len = INT_HEADER_LEN_WORD;

        // insert INT header
        hdr.int_header.setValid();
        hdr.int_header.ver = 0;
        hdr.int_header.rep = 0;
        hdr.int_header.c = 0;  // copy bit
        hdr.int_header.e = 0;  // Max hop count exceeded
        hdr.int_header.m = 0;  // MTU exceeded
        hdr.int_header.rsvd1 = 0; // to track header stack
        hdr.int_header.rsvd2 = 0;
        hdr.int_header.ins_cnt = ins_cnt; // Number of instructions that are set in instruction bitmap
        hdr.int_header.remaining_hop_cnt = REMAINING_HOP_CNT;
        hdr.int_header.instruction_mask_0003 = ins_mask0003;
        hdr.int_header.instruction_mask_0407 = ins_mask0407;
        hdr.int_header.instruction_mask_0811 = 0; // not supported
        hdr.int_header.instruction_mask_1215 = 0; // not supported
        hdr.int_header.rsvd3 = 0;

        // insert INT tail header
        hdr.intl4_tail.setValid();
        hdr.intl4_tail.next_proto = hdr.ipv4.protocol;
        hdr.intl4_tail.dest_port = hdr.udp.dport;
        hdr.intl4_tail.dscp = (bit<8>) hdr.ipv4.dscp;


        hdr.ipv4.totalLen = hdr.ipv4.totalLen + 16; // 16 bytes of INT headers are added to packet INT shim header(4B) + INT tail header(4B) + Int Metadat header(8B)  Rest INT stack will be added by the INT transit hops
        hdr.udp.len = hdr.udp.len + 16;

    }

    action set_hash(bit<16> ecmp_base, bit<32> ecmp_count) {
        hash(hdr.int_header.rsvd3,
	    HashAlgorithm.crc16,
	    ecmp_base,
	    { hdr.ipv4.srcAddr,
	      hdr.ipv4.dstAddr,
          hdr.ipv4.protocol,
          // hdr.tcp.srcPort,
          // hdr.tcp.dstPort },
          hdr.udp.sport,
          hdr.udp.dport },
	           ecmp_count);
    }

    action int_source_dscp(bit<5> ins_cnt, bit<4> ins_mask0003,bit<4> ins_mask0407,bit<16> ecmp_base, bit<32> ecmp_count) {
        int_source(ins_cnt, ins_mask0003,ins_mask0407);
        set_hash(ecmp_base,ecmp_count);
        hdr.ipv4.dscp = INT_DSCP;
    }


    table tb_int_source {
        key = { }
        actions = {
            int_source_dscp;
            set_hash;
        }
        size = 1024;
    }

    apply {
        tb_int_source.apply();
    }
}


//---------------------------------------------------------------------------------------
control IngressImpl(inout headers hdr, inout metadata meta,
inout standard_metadata_t standard_metadata)
{
    action drop() {
        mark_to_drop();
    }

    action ipv4_forward(macAddr_t dmac, bit<9> out_port){
        standard_metadata.egress_spec = out_port;
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dmac;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }
    table ipv4_lpm {
        key = {
            hdr.ipv4.srcAddr : exact;
            hdr.ipv4.dstAddr: lpm;
            hdr.udp.sport : exact;
            hdr.udp.dport : exact;
            // hdr.tcp.srcPort : exact;
            // hdr.tcp.dstPort : exact;
        }
        actions = {
            ipv4_forward;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = NoAction();
    }
    apply{
        if(standard_metadata.ingress_port==1 || standard_metadata.ingress_port==2){
            // initialize the INT header fields
            process_int_source_headers.apply(hdr, meta, standard_metadata); // sets the INT header fields

        }
        // otherwise route the packet to the next hop based on the destination address
        if (hdr.ipv4.isValid() ){
            ipv4_lpm.apply();
        }
    }
}
control EgressImpl(inout headers hdr, inout metadata meta,
inout standard_metadata_t standard_metadata)
{
    apply{
        if(standard_metadata.ingress_port==1 || standard_metadata.ingress_port==2 ){
            Int_transit_egress.apply(hdr, meta, standard_metadata); //sets the INT stack to get metadata from the source switches
        }
    }
}

V1Switch(
        ParserImpl(),
        verify_checksum_control(),
        IngressImpl(),
        EgressImpl(),
        compute_checksum_control(),
        DeparserImpl()
    ) main;
