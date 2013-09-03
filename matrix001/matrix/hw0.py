# Please fill out this stencil and submit using the provided submission script.





## Problem 1
def myFilter(L, num): return [i for i in L if i % num != 0]



## Problem 2
def myLists(L): return [ range(1,i+1) for i in L ]



## Problem 3
def myFunctionComposition(f, g): return { x:z for y2,z in g.items() for x,y1 in f.items() if y1==y2}


## Problem 4
# Please only enter your numerical solution.

complex_addition_a = 5 + 3j
complex_addition_b = 1j
complex_addition_c = -1 + .001j
complex_addition_d = 4.001 + 9j



## Problem 5
GF2_sum_1 = 1
GF2_sum_2 = 0
GF2_sum_3 = 0


## Problem 6
def mySum(L):
    current = 0
    for x in L:
        current += x
    return current



## Problem 7
def myProduct(L):
    current = 1
    for x in L:
        current *= x
    return current



## Problem 8
def myMin(L):
    current = None
    for x in L:
        if current is None:
            current = x
        elif x < current:
            current = x
    return current



## Problem 9
def myConcat(L):
    current = ''
    for x in L:
        current += x
    return current



## Problem 10
def myUnion(L):
    current = set()
    for x in L:
        current |= x
    return current

