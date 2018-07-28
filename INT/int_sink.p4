/********************************************************************
* int_sink.p4: tables, actions, and control flow
*******************************************************************/
#include <core.p4>
#include <v1model.p4>
#include "includes/headers.p4"
#include "includes/parser.p4"
#include "includes/checksums.p4"
#include "includes/int_definitions.p4"
#include "int_transit_source_common.p4"

control process_int_clone (inout headers hdr,inout metadata meta,inout standard_metadata_t standard_metadata) {
    // mon_dest_ip is the destination ip of the monitoring engine
    //mon_dmac is the destination mac of the monitoring engine
    action set_mon_params(macAddr_t mon_dmac){
        hdr.ethernet.dstAddr = mon_dmac;
        //hdr.ipv4.dstAddr = mon_dest_ip;
    }
    table tb_generate_report {
        key = {
            standard_metadata.instance_type: exact;
        }
        actions = {
            set_mon_params;
        }
    }
    apply {
        tb_generate_report.apply();
    }
}

control process_int_sink (inout headers hdr,inout metadata meta,inout standard_metadata_t standard_metadata) {
    action restore_header () {
        hdr.udp.dport = hdr.intl4_tail.dest_port;
        hdr.ipv4.dscp = (bit<6>)hdr.intl4_tail.dscp;
    }

    action int_sink() {
        // restore length fields of IPv4 header and UDP header
        hdr.ipv4.totalLen = hdr.ipv4.totalLen - (bit<16>)((hdr.intl4_shim.len - (bit<8>)hdr.int_header.ins_cnt) << 2);
        hdr.udp.len = hdr.udp.len - (bit<16>)((hdr.intl4_shim.len - (bit<8>)hdr.int_header.ins_cnt) << 2);
        // remove all the INT information from the packet
        hdr.int_header.setInvalid();
        hdr.int_data.setInvalid();
        hdr.intl4_shim.setInvalid();
        hdr.intl4_tail.setInvalid();
        //hdr.int_switch_id.setInvalid();
        //hdr.int_port_ids.setInvalid();

        //hdr.int_hop_latency.setInvalid();
        //hdr.int_q_occupancy.setInvalid();
        //hdr.int_ingress_tstamp.setInvalid();
        //hdr.int_egress_tstamp.setInvalid();
        //hdr.int_q_congestion.setInvalid();
        //hdr.int_egress_port_tx_util.setInvalid();
    }

    apply {
            restore_header();
            int_sink();
    }
}
//---------------------INGRESS ---------------------------------------
control IngressImpl(inout headers hdr, inout metadata meta,inout standard_metadata_t standard_metadata)
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
            hdr.ipv4.dstAddr: lpm;
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
     //clone packet from ingress to egress
        if(standard_metadata.ingress_port==3){
            clone(CloneType.I2E, CLONE_SESSION_ID);

            // if (hdr.ipv4.isValid()) {
            //         ipv4_lpm.apply();
             //}
             //Int_transit_egress.apply(hdr, meta, standard_metadata);
             // if (hdr.ipv4.isValid()) {
                //      ipv4_lpm.apply();
              //}

             process_int_sink.apply(hdr, meta, standard_metadata);

        }

            if (hdr.ipv4.isValid()) {
                    ipv4_lpm.apply();
            }








    }
}

//---------------------EGRESS ---------------------------------------
control EgressImpl(inout headers hdr, inout metadata meta,inout standard_metadata_t standard_metadata)
{
    apply{
        if(standard_metadata.ingress_port==3){
            if(standard_metadata.instance_type == 1){
                process_int_clone.apply(hdr,meta,standard_metadata);
            }
            else {
                //process_int_sink.apply(hdr, meta, standard_metadata);
            }

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
