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

ratings = [
    [0, 5, 5, 3, 2, 5, 2, 2, 3, 5],
    [4, 0, 1, 5, 1, 3, 1, 3, 5, 5],
    [4, 3, 0, 1, 3, 5, 3, 1, 5, 4],
    [5, 5, 5, 0, 4, 5, 4, 5, 1, 5],
    [4, 5, 1, 3, 0, 2, 5, 4, 3, 3],
    [5, 5, 1, 4, 1, 0, 4, 2, 2, 3],
    [4, 1, 1, 1, 1, 2, 0, 5, 2, 5],
    [5, 2, 3, 4, 3, 4, 5, 0, 4, 4],
    [2, 2, 3, 1, 4, 5, 5, 4, 0, 1],
    [4, 2, 5, 2, 3, 4, 1, 3, 2, 0]
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
        x = vec[i]
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

def dormcost2(vec, debug=False):
    slots = [0,0,1,1,2,2,3,3,4,4]

    occupy = {}
    for i, x in enumerate(vec):
        dorm = slots[x]
        occupy.setdefault(dorm, [])
        occupy[dorm].append(i)
        del slots[x]

    cost = 0
    for dorm, (p1, p2) in occupy.items():
        cost += 3-ratings[p1][p2]
        cost += 3-ratings[p2][p1]
        if debug:
            print cost, dorms[dorm], prefs[p1][0], prefs[p2][0], ratings[p1][p2], ratings[p2][p1]
    return cost




if __name__ == '__main__':
    import optimization as opt
    '''
    s = opt.random_optimize(domain, dormcost)
    print s
    print dormcost(s)
    print_solution(s)

    s = opt.genetic_optimize(domain, dormcost)
    print s
    print dormcost(s)
    print_solution(s)
    '''

    s = opt.genetic_optimize(domain, dormcost2)
    print s
    print dormcost2(s, 1)
    print_solution(s)
