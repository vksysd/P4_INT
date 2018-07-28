cp ../../INT_udp_flows_results_from_h1.txt .
rm INT_udp_flows_results.txt
head -n 90000 INT_udp_flows_results_from_h1.txt >> INT_udp_flows_results.txt

