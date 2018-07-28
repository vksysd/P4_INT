awk '{print $1" "$5}' s1.txt >> s1_latency.txt
awk '{print $1" "$5}' s2.txt >> s2_latency.txt
awk '{print $1" "$5}' s3.txt >> s3_latency.txt
awk '{print $1" "$5}' s4.txt >> s4_latency.txt

awk '{print $1" "$7}' s1.txt >> s1_qlength.txt
awk '{print $1" "$7}' s2.txt >> s2_qlength.txt
awk '{print $1" "$7}' s3.txt >> s3_qlength.txt
awk '{print $1" "$7}' s4.txt >> s4_qlength.txt