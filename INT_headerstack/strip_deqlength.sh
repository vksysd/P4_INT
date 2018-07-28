#remove deq_depth column from file INT_udp_results
awk '{print $8}' INT_udp_results.txt > deq_depth.txt
