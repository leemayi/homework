'''
Question 1
(seed = 696320)
Download http://coursera.cs.princeton.edu/algs4/Timing.class

Using the value 696320 for the seed, estimate the order of growth of the running time
of the function call Timing.trial(N, seed) as a function of N. To do so, write a program that
calls Timing.trial(N, seed) for different values of N and measures how long each function call
takes (e.g., via the Stopwatch library in algs4.jar). Then, formulate a doubling hypothesis to
estimate the order of growth.

Assume that the running time obeys a power law T(N) ~ a N^b. For your answer, enter the
constant b. Your answer will be marked as correct if it is within 5% of the target answer -
we recommend using two digits after the decimal separator, e.g., 2.34.
'''

import sys
import time
import math

import Timing

seed = 696320
N = 4096

print '%10s%10s%10s%10s' % ('N', 'cost(s)', 'ratio', 'lg ratio')
prev_cost = None

for i in range(6):
    st = time.time()
    Timing.trial(N, seed)
    cost = time.time() - st

    if prev_cost:
        ratio = cost / prev_cost
        print '%10d%10.2f%10.2f%10.2f' % (N, cost, ratio, math.log(ratio)/math.log(2))
    else:
        print '%10d%10.2f' % (N, cost)

    N *= 2
    prev_cost = cost


'''
$ jython ex1.py 
         N   cost(s)     ratio  lg ratio
     10000      0.88
     20000      1.51      1.70      0.77
     40000      4.29      2.85      1.51
     80000     12.80      2.98      1.58
    160000     38.32      2.99      1.58
    320000    106.92      2.79      1.48

$ jython ex1.py 
         N   cost(s)     ratio  lg ratio
      4096      0.51
      8192      0.40      0.79     -0.34
     16384      1.01      2.51      1.33
     32768      3.19      3.15      1.65
     65536      8.99      2.82      1.50
    131072     25.77      2.87      1.52
'''
