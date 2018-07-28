#plotting latency experienced by the mice and elephant flow packet as sum of individual latency on switches

import numpy as np
import matplotlib.pyplot as plt
 
# data to plot
n_groups = 4
#plot 50-50 baseline,with rate limit and 75-25 baseline,with rate limit
means_mouse = (6717.298291308138, 460.105,7786.208648034887 ,479.3333333333333 )
means_elephant = (6720.383931729399, 248.21981657055252, 7964.18449664444, 1367.6666666666667)
 
# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8
 
rects1 = plt.bar(index, means_elephant, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Elephant Flow')
 
rects2 = plt.bar(index + bar_width, means_mouse, bar_width,
                 alpha=opacity,
                 color='g',
                 label='Mouse Flow')
 
plt.xlabel('Ratio of elephant : mouse flows')
plt.ylabel('Average Latency(in ms)')
plt.title('Average latency of elephant and mouse flow packet')
plt.xticks(index + bar_width, ('Case A', 'Case B', 'Case C', 'Case D'))
plt.legend()
 
plt.tight_layout()
plt.savefig('avg_latency.png')
plt.show()
