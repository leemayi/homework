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
        name = optimizer.__name__
        print 'evaluating', name, '...'
        row = []
        for _ in range(n):
            start = time.time()
            sol = optimizer(domain, costf)
            time_cost = time.time() - start
            row.append((costf(sol), time_cost, sol))
        sols.append((name, row))

    print 'for', n, 'times'
    for name, row in sols:
        costs = [i[0] for i in row]
        tcosts = [i[1] for i in row]

        print '-'*10, name
        print 'best:', min(costs)
        print 'time cost:', sum(tcosts)
        print 'worst:', max(costs)

def annealing_optimize(domain, costf, T=10000., cool=0.95, step=1):
    vec = [random.randint(*d) for d in domain]

    while T>.1:
        i = random.randint(0, len(domain)-1)
        dir_ = random.randint(-step, step)
        vecb = vec[:]
        vecb[i] += dir_

        low, high = domain[i]
        if vecb[i] < low:
            vecb[i] = low
        elif vecb[i] > high:
            vecb[i] = high

        ea = costf(vec)
        eb = costf(vecb)

        if (eb < ea or random.random() < pow(math.e, -(eb-ea)/T)):
            vec = vecb

        T *= cool
    return vec

def genetic_optimize(domain, costf, popsize=50, step=1, mutprob=.2, elite=.2, maxiter=100):

    def mutate(vec):
        i = random.randint(0, len(domain)-1)
        low, high = domain[i]
        if vec[i] > low:
            return vec[:i] + [vec[i]-step] + vec[i+1:]
        elif vec[i] < high:
            return vec[:i] + [vec[i]+step] + vec[i+1:]

    def crossover(r1, r2):
        i = random.randint(1, len(domain)-2)
        return r1[:i] + r2[i:]

    pop = [[random.randint(*d) for d in domain]
        for _ in range(popsize)]
    top = int(elite*popsize)

    for i in range(maxiter):
        scores = [(costf(v), v) for v in pop]
        scores.sort()
        ranked = [v for (s,v) in scores]

        pop = ranked[:top]

        while len(pop) < popsize:
            if random.random() < mutprob:
                c = random.randint(0, top-1)
                pop.append(mutate(ranked[c]))
            else:
                c1 = random.randint(0, top-1)
                c2 = random.randint(0, top-1)
                pop.append(crossover(ranked[c1], ranked[c2]))
    return scores[0][1]



if __name__ == '__main__':
    s = [1,4,3,2,7,3,6,3,2,4,5,3]
    print schedule_cost(s)

    domain = [(0,9)]*(len(people)*2)
    evaluate(domain, schedule_cost,[
        genetic_optimize,
        annealing_optimize,
        hill_climb,
        random_optimize,
        ], 3)
    
