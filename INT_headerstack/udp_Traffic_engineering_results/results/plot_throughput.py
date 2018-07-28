#plotting th as no of packets received per sec with INT and without INT

import numpy as np
import matplotlib.pyplot as plt
 
# data to plot
n_groups = 2
#plot 50-50 baseline,with rate limit and 75-25 baseline,with rate limit
th_without_INT = (150,121 )
th_with_INT = (225,190)
 
# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8
 
rects1 = plt.bar(index,th_without_INT, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Throughput without INT module')
 
rects2 = plt.bar(index + bar_width,th_with_INT, bar_width,
                 alpha=opacity,
                 color='g',
                 label='Throughput with INT module')
 
plt.xlabel('Ratio of elephant : mouse flows')
plt.ylabel('Average Throughput(#pkts received/sec)')
plt.title('Average Throughput with and without INT')
plt.xticks(index + bar_width, ('Case A(50:50)', 'Case B(75:25)'))
plt.legend()
 
plt.tight_layout()
plt.savefig('avg_th.png')
plt.show()
