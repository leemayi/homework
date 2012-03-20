import random
import sys

def base26(strn):
    sz = len(strn)
    s, p = 0, 1
    for i in range(sz-1, -1, -1):
        s += (ord(strn[i]) - ord('a') + 1)*p
        p *= 26
    return s

def missing_one(data, a):
    s = 0
    for i in range(1, len(data)):
        s ^= data[i]
    for i in range(a, a+len(data)):
        s ^= i
    return s

def test_missing_one():
    n, a = 6, 2
    data = range(a, a+n)
    random.shuffle(data)
    m = data[0]
    data[0] = -1
    l = missing_one(data, a)
    print data, m, l
    assert m == l

def func(n):
    if (n==1):
        return 0
    if (n%2 == 0):
        return 1 + func(n/2)
    x = func(n+1)
    y = func(n-1)
    return min(x, y)+1


