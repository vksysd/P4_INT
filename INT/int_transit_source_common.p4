// this is a common file which contains some control functions which are imported both in int_source as well as int_transit files
/********************************************************************
* int_transit_source_common.p4: tables, actions, and control flow
*******************************************************************/
#include <core.p4>
#include <v1model.p4>
#include "includes/headers.p4"
#include "includes/parser.p4"
#include "includes/checksums.p4"


control Int_metadata_insert(inout headers hdr, in int_metadata_t int_metadata,inout standard_metadata_t standard_metadata)
{
        /* this reference implementation covers only INT instructions 0-3 */
        action int_set_header_0() { // switch id
            hdr.int_switch_id.setValid();
            hdr.int_switch_id.switch_id = int_metadata.switch_id;
        }
        action int_set_header_1() {  // ingress and egress ports
            hdr.int_port_ids.setValid();
            hdr.int_port_ids.ingress_port_id =
                (bit<16>) standard_metadata.ingress_port;
            hdr.int_port_ids.egress_port_id =
                (bit<16>) standard_metadata.egress_port;
        }
        action int_set_header_2() { // hop latency
            hdr.int_hop_latency.setValid();
            hdr.int_hop_latency.hop_latency =
                (bit<32>) standard_metadata.deq_timedelta; //the time, in microseconds, that the packet spent in the queue.
        }
        action int_set_header_3() { // q occupency
            hdr.int_q_occupancy.setValid();
            hdr.int_q_occupancy.q_id = 0; // assuming qid is always 0
                //(bit<8>) standard_metadata.egress_qid; // egress qid is not yet exposed in v1model.p4
            hdr.int_q_occupancy.q_occupancy =
                (bit<24>) standard_metadata.deq_qdepth; //the depth of queue when the packet was dequeued.
        }
        action int_set_header_4() { //ingress_timestamp
            hdr.int_ingress_tstamp.setValid();
            hdr.int_ingress_tstamp.ingress_tstamp =
            (bit<32>) standard_metadata.enq_timestamp;
        }
        action int_set_header_5() { //egress_timestamp
            hdr.int_egress_tstamp.setValid();
            hdr.int_egress_tstamp.egress_tstamp =
            (bit<32>) standard_metadata.enq_timestamp +
            (bit<32>) standard_metadata.deq_timedelta;
        }
        action int_set_header_6() { //q_congestion
            // TODO: implement queue congestion support in BMv2
            // TODO: update egress queue ID
            hdr.int_q_congestion.setValid();
            hdr.int_q_congestion.q_id =
            0;
            // (bit<8>) standard_metadata.egress_qid;
            hdr.int_q_congestion.q_congestion =
            // (bit<24>) queueing_metadata.deq_congestion;
            0;
        }
        action int_set_header_7() { //egress_port_tx_utilization
            // TODO: implement tx utilization support in BMv2
            hdr.int_egress_port_tx_util.setValid();
            hdr.int_egress_port_tx_util.egress_port_tx_util =
            // (bit<32>) queueing_metadata.tx_utilization;
            0;
        }


        /* action functions for bits 0-3 combinations, 0 is msb, 3 is lsb */
        /* Each bit set indicates that corresponding INT header should be added */
        action int_set_header_0003_i0() {
        }
        action int_set_header_0003_i1() {
            int_set_header_3();
        }
        action int_set_header_0003_i2() {
            int_set_header_2();
        }
        action int_set_header_0003_i3() {
            int_set_header_3();
            int_set_header_2();
        }
        action int_set_header_0003_i4() {
            int_set_header_1();
        }
        action int_set_header_0003_i5() {
            int_set_header_3();
            int_set_header_1();
        }
        action int_set_header_0003_i6() {
            int_set_header_2();
            int_set_header_1();
        }
        action int_set_header_0003_i7() {
            int_set_header_3();
            int_set_header_2();
            int_set_header_1();
        }
        action int_set_header_0003_i8() {
            int_set_header_0();
        }
        action int_set_header_0003_i9() {
            int_set_header_3();
            int_set_header_0();
        }
        action int_set_header_0003_i10() {
            int_set_header_2();
            int_set_header_0();
        }
        action int_set_header_0003_i11() {
            int_set_header_3();
            int_set_header_2();
            int_set_header_0();
        }
        action int_set_header_0003_i12() {
            int_set_header_1();
            int_set_header_0();
        }
        action int_set_header_0003_i13() {
            int_set_header_3();
            int_set_header_1();
            int_set_header_0();
        }
        action int_set_header_0003_i14() {
            int_set_header_2();
            int_set_header_1();
            int_set_header_0();
        }
        action int_set_header_0003_i15() {
            int_set_header_3();
            int_set_header_2();
            int_set_header_1();
            int_set_header_0();
        }
        /* action function for bits 4-7 combinations, 4 is msb, 7 is lsb */
        action int_set_header_0407_i0() {
        }
        action int_set_header_0407_i1() {
            int_set_header_7();
        }
        action int_set_header_0407_i2() {
            int_set_header_6();
        }
        action int_set_header_0407_i3() {
            int_set_header_7();
            int_set_header_6();
        }
        action int_set_header_0407_i4() {
            int_set_header_5();
        }
        action int_set_header_0407_i5() {
            int_set_header_7();
            int_set_header_5();
        }
        action int_set_header_0407_i6() {
            int_set_header_6();
            int_set_header_5();
        }
        action int_set_header_0407_i7() {
            int_set_header_7();
            int_set_header_6();
            int_set_header_5();
        }
        action int_set_header_0407_i8() {
            int_set_header_4();
        }
        action int_set_header_0407_i9() {
            int_set_header_7();
            int_set_header_4();
        }
        action int_set_header_0407_i10() {
            int_set_header_6();
            int_set_header_4();
        }
        action int_set_header_0407_i11() {
            int_set_header_7();
            int_set_header_6();
            int_set_header_4();
        }
        action int_set_header_0407_i12() {
            int_set_header_5();
            int_set_header_4();
        }
        action int_set_header_0407_i13() {
            int_set_header_7();
            int_set_header_5();
            int_set_header_4();
        }
        action int_set_header_0407_i14() {
            int_set_header_6();
            int_set_header_5();
            int_set_header_4();
        }
        action int_set_header_0407_i15() {
            int_set_header_7();
            int_set_header_6();
            int_set_header_5();
            int_set_header_4();
        }
        /* Table to process instruction bits 0-3 */
        table int_inst_0003 {
            key = {
                hdr.int_header.instruction_mask_0003 : exact;
            }
            actions = {
                int_set_header_0003_i0;
                int_set_header_0003_i1;
                int_set_header_0003_i2;
                int_set_header_0003_i3;
                int_set_header_0003_i4;
                int_set_header_0003_i5;
                int_set_header_0003_i6;
                int_set_header_0003_i7;
                int_set_header_0003_i8;
                int_set_header_0003_i9;
                int_set_header_0003_i10;
                int_set_header_0003_i11;
                int_set_header_0003_i12;
                int_set_header_0003_i13;
                int_set_header_0003_i14;
                int_set_header_0003_i15;
            }
            default_action = int_set_header_0003_i0();
            size = 16;
        }
        /* Table to process instruction bits 4-7 */
        table int_inst_0407 {
            key = {
                hdr.int_header.instruction_mask_0407 : exact;
            }
            actions = {
                int_set_header_0407_i0;
                int_set_header_0407_i1;
                int_set_header_0407_i2;
                int_set_header_0407_i3;
                int_set_header_0407_i4;
                int_set_header_0407_i5;
                int_set_header_0407_i6;
                int_set_header_0407_i7;
                int_set_header_0407_i8;
                int_set_header_0407_i9;
                int_set_header_0407_i10;
                int_set_header_0407_i11;
                int_set_header_0407_i12;
                int_set_header_0407_i13;
                int_set_header_0407_i14;
                int_set_header_0407_i15;
            }
            default_action = int_set_header_0407_i0();
            size = 16;
        }

        apply{
            int_inst_0003.apply();
            int_inst_0407.apply();
        }
}
control Int_outer_encap(inout headers hdr, in int_metadata_t int_metadata)
{
        action int_update_ipv4() {
            hdr.ipv4.totalLen = hdr.ipv4.totalLen + int_metadata.insert_byte_cnt;
        }
        action int_update_shim() {
            hdr.intl4_shim.len = hdr.intl4_shim.len + int_metadata.int_hdr_word_len;
        }
        apply{
            if (hdr.ipv4.isValid()) {
                int_update_ipv4();
            }
            if (hdr.intl4_shim.isValid()) {
                int_update_shim();
            }
        }
}
/* TBD - Check egress link MTU, do not insert any metadata and
set M bit if adding metadata will cause egress MTU to be exceeded */
control Int_transit_egress(inout headers hdr, inout metadata meta,
inout standard_metadata_t standard_metadata)
{
        action int_transit(bit<32> switch_id) {
            meta.int_metadata.switch_id = switch_id;
            meta.int_metadata.insert_byte_cnt = (bit<16>) hdr.int_header.ins_cnt << 2;
            meta.int_metadata.int_hdr_word_len = (bit<8>) hdr.int_header.ins_cnt;
        }
        table int_prep {
            key = {}
            actions = {int_transit;}
        }
        Int_metadata_insert() int_metadata_insert;
        Int_outer_encap() int_outer_encap;
        action int_hop_cnt_decrement() {
            hdr.int_header.remaining_hop_cnt = hdr.int_header.remaining_hop_cnt - 1;
        }
        action int_hop_cnt_exceeded() {
            hdr.int_header.e = 1;
        }

        apply{
            if(hdr.int_header.isValid()) {
                if(hdr.int_header.remaining_hop_cnt != 0 && hdr.int_header.e == 0) {
                    int_hop_cnt_decrement();
                    int_prep.apply();
                    int_metadata_insert.apply(hdr, meta.int_metadata, standard_metadata);
                    int_outer_encap.apply(hdr, meta.int_metadata);
                }
                else {
                    int_hop_cnt_exceeded();
                }
            }
        }
}
