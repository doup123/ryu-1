# StateA=set([3,4,5,7,8])
# StateB=set([1,2,3,6])
# print StateB-StateA
from pybloom import BloomFilter
import random
from pybloom import ScalableBloomFilter
sbfA=ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH,initial_capacity=10000)
sbfB=ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH,initial_capacity=10000)
common_state=[]
StateA=[]
StateB=[]
add=[]
remove=[]
for i in range(1,10000):
    y=random.randint(1, 10000)
    z=random.randint(1,10000)
    sbfA.add(y)
    sbfB.add(z)
    StateA.append(y)
    StateB.append(z)
for k in range(1,9999):
    #common rules
    if sbfA.__contains__(StateB[k])!=True:
        add.append(StateB[k])
    if sbfB.__contains__(StateA[k])!=True:
        remove.append(StateA[k])

# for j in range(1,1000):
#     x=random.randint(0,1000000)
#     if sbf.__contains__(x):
#         common_state.append(x)
# print common_state
# import timeit
# init = 'temp1 = list(range(1000)); temp2 = [i * 2 for i in range(5000)]'
# print timeit.timeit('list(set(temp1) - set(temp2))', init, number = 100000)
# print timeit.timeit('s = set(temp2);[x for x in temp1 if x not in s]', init, number = 100000)
# print timeit.timeit('[item for item in temp1 if item not in temp2]', init, number = 100000)