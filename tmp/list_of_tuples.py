from collections import defaultdict

l = [(10,20),(10,40),(10,50),(20,4),(20,6),(20,8),(20,40)]
l.append((60,20))
l.append((30,40))
d = defaultdict(int)
for i in [i[0] for i in l]:
    d[i] += 1
result = max(d.items(), key=lambda x: x[1])
print ("result = ",result)
y = sorted([('abc', 121),('abc', 231),('abc', 148), ('abc',221)], key=lambda x: x[1])
print (y)
def most_common(lst):
    return max(set(lst), key=lst.count)
z = (most_common([i[0] for i in l]))
print ("max repeated element is = ",z)
print([i[0] for i in l].index(z))
print(l[3])
print("--------------------------------------------------")
def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items()
                            if len(locs)>1)

# print (list_duplicates([i[0] for i in l]))
for dup in sorted(list_duplicates([i[0] for i in l])):
    print (dup)
print("type dup = ",type(dup))

def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs
print (list_duplicates_of([i[0] for i in l], 10))

for i in list_duplicates_of([i[0] for i in l], 10):
    print(l[i])
