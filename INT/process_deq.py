#!/bin/sh
#!/usr/bin/env python
#this script sums the non zero entries in deq_depth
import os
os.system('./strip_deqlength.sh')
f=open("deq_depth.txt","r")
sum_deq=0
for line in f:
    if int(line) > 0:
        sum_deq = sum_deq + int(line)
        #print line,
print "sum_deq = ", sum_deq
os.system('rm deq_depth.txt')
f.close()
