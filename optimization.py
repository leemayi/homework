import time
import random
import math

people = [
    ('Seymour', 'BOS'),
    ('Franny', 'DAL'),
    ('Zooey', 'CAK'),
    ('Walt', 'MIA'),
    ('Buddy', 'ORD'),
    ('Les', 'OMA')]

destination = 'LGA'

flights = {}
with open('data/schedule.txt') as f:
    for line in f:
        origin, dest, depart, arrive, price = line.rstrip().split(',')
        flights.setdefault((origin, dest), [])

        flights[(origin, dest)].append((depart, arrive, int(price)))

def get_minutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3]*60+x[4]

def print_schedule(r):
    for d, (name, origin) in enumerate(people):
        out = flights[(origin, destination)][r[2*d]]
        ret = flights[(destination, origin)][r[2*d+1]]
        print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name, origin,
            out[0], out[1], out[2],
            ret[0], ret[1], ret[2])

def schedule_cost(r):
    total_price = 0
    latest_arrival = 0
    earliest_dep = 24*60

    for d, (name, origin) in enumerate(people):
        outbound = flights[(origin, destination)][r[2*d]]
        returnf = flights[(destination, origin)][r[2*d+1]]

        total_price += outbound[2]+returnf[2]

        latest_arrival = max(latest_arrival, get_minutes(outbound[1]))
        earliest_dep = min(earliest_dep, get_minutes(returnf[0]))

    total_wait = 0
    for d, (name, origin) in enumerate(people):
        outbound = flights[(origin, destination)][r[2*d]]
        returnf = flights[(destination, origin)][r[2*d+1]]

        total_wait += latest_arrival - get_minutes(outbound[1])
        total_wait += get_minutes(returnf[0]) - earliest_dep

    if latest_arrival > earliest_dep:
        total_price += 50

    return total_price + total_wait

def random_optimize(domain, costf):
    best = 999999999
    bestr = None
    for i in range(1000):
        r = [random.randint(*d) for d in domain]
        cost = costf(r)
        if cost < best:
            best = cost
            bestr = r
    return bestr

def hill_climb(domain, costf):
    r = [random.randint(*d) for d in domain]
    #for _ in range(100000):
    while 1:
        neighbors = []
        for i, (low, high) in enumerate(domain):
            if r[i] > low:
                neighbors.append(r[0:i] + [r[i]-1] + r[i+1:])
            if r[i] < high:
                neighbors.append(r[0:i] + [r[i]+1] + r[i+1:])

        current = costf(r)
        best = current
        for i, neighbor in enumerate(neighbors):
            cost = costf(neighbor)
            if cost < best:
                best = cost
                r = neighbor

        if best == current:
            break
    return r

def evaluate(domain, costf, optimizers, n=5):
    sols = []
    for optimizer in optimizers:
        row = []
        for _ in range(n):
            start = time.time()
            sol = optimizer(domain, costf)
            time_cost = time.time() - start
            row.append((costf(sol), time_cost, sol))
        sols.append((optimizer.__name__, row))

    for name, row in sols:
        costs = [i[0] for i in row]
        tcosts = [i[1] for i in row]

        print '-'*4, name
        print 'best:', min(costs)
        print 'time cost:', sum(tcosts)
        print 'worst:', max(costs)

def annealing_optimize(domain, costf, T=10000., cool=0.95, step=1):
    pass

        



if __name__ == '__main__':
    s = [1,4,3,2,7,3,6,3,2,4,5,3]
    print schedule_cost(s)

    domain = [(0,9)]*(len(people)*2)
    evaluate(domain, schedule_cost, [random_optimize, hill_climb])
    
