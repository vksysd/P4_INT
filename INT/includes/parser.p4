/********************************************************************
* parser.p4
*******************************************************************/
/* -*- P4_16 -*- */
#ifndef __INT_PARSER__
#define __INT_PARSER__

#include "int_definitions.p4"

parser ParserImpl(packet_in packet, out headers hdr, inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
        state start {
                transition parse_ethernet;
        }
        state parse_ethernet {
                packet.extract(hdr.ethernet);
                transition select(hdr.ethernet.etherType) {
                        ETH_TYPE_IPV4: parse_ipv4;
                        default: accept;
        }
        }
        state parse_ipv4 {
                packet.extract(hdr.ipv4);
                transition select(hdr.ipv4.protocol) {
                        IP_PROTO_TCP: parse_tcp;
                        IP_PROTO_UDP : parse_udp;
                        default: accept;
                }
        }
        state parse_tcp {
                packet.extract(hdr.tcp);
                transition select((hdr.ipv4.dscp & INT_DSCP) == INT_DSCP) {
                    true: parse_intl4_shim;
                    default: accept;
                }
        }
        state parse_udp {
                packet.extract(hdr.udp);
                //transition parse_intl4_shim;
                transition select((hdr.ipv4.dscp & INT_DSCP) == INT_DSCP) {
                    true: parse_intl4_shim;
                    default: accept;
                }
        }
        state parse_intl4_shim {
                packet.extract(hdr.intl4_shim);
                transition parse_int_header;
        }
        state parse_int_header {
                packet.extract(hdr.int_header);
                transition select(hdr.intl4_shim.len - INT_HEADER_LEN_WORD){
                    0 : parse_intl4_tail;
                    default : parse_int_data;
                }

        }
        state parse_int_data {
            // Parse INT metadata, not INT header, INT shim header and INT tail header
            packet.extract(hdr.int_data, (bit<32>) ((hdr.intl4_shim.len - INT_HEADER_LEN_WORD) << 5));
            transition parse_intl4_tail;
        }
        state parse_intl4_tail {
                packet.extract(hdr.intl4_tail);
                transition accept;
        }
}
control DeparserImpl(packet_out packet, in headers hdr) {
    apply {
            packet.emit(hdr.ethernet);
            packet.emit(hdr.ipv4);
            packet.emit(hdr.tcp);
            packet.emit(hdr.udp);
            packet.emit(hdr.intl4_shim);
            packet.emit(hdr.int_header);
            packet.emit(hdr.int_switch_id);
            packet.emit(hdr.int_port_ids);
            packet.emit(hdr.int_hop_latency);
            packet.emit(hdr.int_q_occupancy);
            packet.emit(hdr.int_ingress_tstamp);
            packet.emit(hdr.int_egress_tstamp);
            packet.emit(hdr.int_q_congestion);
            packet.emit(hdr.int_egress_port_tx_util);
            packet.emit(hdr.int_data);
            packet.emit(hdr.intl4_tail);
            }
}
#endif
