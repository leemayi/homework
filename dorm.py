import sys
import random
import math

Z, A, H, B, P = 'Zeus', 'Athena', 'Hercules', 'Bacchus', 'Pluto'
dorms = [Z,A,H,B,P]

prefs = [
    ('Toby',   (B, H)),
    ('Steve',  (Z, P)),
    ('Andrea', (A, Z)),
    ('Sarah',  (Z, P)),
    ('Dave',   (A, B)),
    ('Jeff',   (H, P)),
    ('Fred',   (P, A)),
    ('Suzie',  (B, H)),
    ('Laura',  (B, H)),
    ('Neil',   (H, A)),
    ]

domain = [(0,(len(dorms)*2)-i-1) for i in range(len(dorms)*2)]

def print_solution(vec):
    slots = []
    for i in range(len(dorms)):
        slots += [i, i]

    for i, (name, (pref1, pref2)) in enumerate(prefs):
        x = vec[i]
        dorm = dorms[slots[x]]
        print name, dorm
        del slots[x]

def dormcost(vec):
    cost = 0
    slots = [0,0,1,1,2,2,3,3,4,4]

    for i in range(len(vec)):
        x = int(vec[i])
        dorm = dorms[slots[x]]
        pref = prefs[i][1]

        if pref[0] == dorm:
            pass
        elif pref[1] == dorm:
            cost += 1
        else:
            cost += 3
        del slots[x]

    return cost





if __name__ == '__main__':
    import optimization as opt
    s = opt.random_optimize(domain, dormcost)
    print s
    print dormcost(s)
    print_solution(s)

    s = opt.genetic_optimize(domain, dormcost)
    print s
    print dormcost(s)
    print_solution(s)

