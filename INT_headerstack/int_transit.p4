/********************************************************************
* int_transit.p4: tables, actions, and control flow
*******************************************************************/
#include <core.p4>
#include <v1model.p4>
#include "includes/headers.p4"
#include "includes/parser.p4"
#include "includes/checksums.p4"
#include "int_transit_source_common.p4"

control IngressImpl(inout headers hdr, inout metadata meta,
inout standard_metadata_t standard_metadata)
{
    action drop() {
        mark_to_drop();
    }

    action ipv4_forward(macAddr_t dmac,bit<9> out_port){
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

        if (hdr.ipv4.isValid()) {
                ipv4_lpm.apply();
        }

    }
}
control EgressImpl(inout headers hdr, inout metadata meta,inout standard_metadata_t standard_metadata)
{
    apply{
        if(standard_metadata.ingress_port != 5){
            Int_transit_egress.apply(hdr, meta, standard_metadata);

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
