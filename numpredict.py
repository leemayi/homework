from random import random, randint
import math

def wineprice(rating, age):
    peak_age = rating - 50
    price = rating / 2

    if age > peak_age:
        price = price * (5 - (age - peak_age))
    else:
        price = price * (5 * ((age+1)/peak_age))

    return max(price, 0)

def wineset1():
    rows = []
    for i in range(300):
        rating = random() * 50 + 50
        age = random() * 50

        price = wineprice(rating, age)
        price *= (random() * .4 + .8)

        rows.append({'input': (rating, age),
            'result': price})
    return rows

def euclidean(v1, v2):
    return math.sqrt(sum([ ((v1[i]-v2[i])**2) for i in range(len(v1)) ]))

def getdistances(data, v1):
    dl = [ (euclidean(v1, wine['input']), i) for i, wine in enumerate(data) ]
    dl.sort()
    return dl

def knnestimate(data, v1, k=5):
    dlist = getdistances(data, v1)
    avg = 0.
    for i in range(k):
        idx = dlist[i][1]
        avg += data[idx]['result']
    avg /= k
    return avg

def gaussian(dist, sigma=10.):
    return math.e ** -(dist**2/(2 * sigma**2))

def weightedknn(data, v1, k=5, weightf=gaussian):
    dlist = getdistances(data, v1)
    avg = 0.
    totalweight = 0.

    for i in range(k):
        dist, idx = dlist[i]
        weight = weightf(dist)
        avg += weight * data[idx]['result']
        totalweight += weight
    avg /= totalweight
    return avg

def dividedata(data, test=.05):
    trainset = []
    testset = []
    for row in data:
        if random() < test:
            testset.append(row)
        else:
            trainset.append(row)
    return trainset, testset

def testalgorithm(algf, trainset, testset):
    error = 0.
    for row in testset:
        guess = algf(trainset, row['input'])
        error += (row['result']-guess)**2
    return error/len(testset)

def crossvalidate(algf, data, trials=100, test=.05):
    error = 0.
    for i in range(trials):
        trainset, testset = dividedata(data, test)
        error += testalgorithm(algf, trainset, testset)
    return error/trials

def wineset2():
    rows = []
    for i in range(300):
        rating = random() * 50 + 50
        age = random() * 50
        aisle = float(randint(1, 20))
        bottlesize = [375., 750., 1500., 3000,][randint(0,3)]
        price = wineprice(rating, age)
        price *= (bottlesize/750)
        price *= (random()*.9+.2)
        rows.append({'input': (rating, age, aisle, bottlesize),
            'result': price})
    return rows

def rescale(data, scale):
    scaleddata = []
    for row in data:
        scaled = [scale[i]*row['input'][i] for i in range(len(scale))]
        scaleddata.append({'input':scaled, 'result':row['result']})
    return scaleddata

def createcostfunction(algf, data):
    def costf(scale):
        sdata = rescale(data, scale)
        return crossvalidate(algf, sdata, trials=10)
    return costf

def createcostfunction2(algf, data):
    def costf(scale):
        sdata = rescale(data, scale[:-1])
        def foo(*args, **kw):
            return algf(*args, k=scale[-1], **kw)
        return crossvalidate(foo, sdata, trials=10)
    return costf

weightdomain = [(0,20)]*4
weightdomain2 = weightdomain + [(3,10)]

def wineset3():
    rows = wineset1()
    for row in rows:
        if random() < .5:
            row['result'] *= .5
    return rows

def probguess(data, v1, low, high, k=5, weightf=gaussian):
    dlist = gestdistances(data, v1)
    nweight = 0.
    tweight = 0.

    for i in range(k):
        dist = dlist[i][0]
        idx = dlist[i][1]
        weight = weightf(dist)
        v = data[idx]['result']

        if v >= low and v <= high:
            nweight += weight
        tweight += weight
    if tweight == 0:
        return 0
    return nweight / tweight

def cumulativegraph(data, v1, high, k=5, weightf=gaussian):
    from pylab import arange, array, plot, show
    t1 = arange(0., high, .1)
    cprob = array([probguess(data, vec1, 0, v, k, weightf) for v in t1])
    plot(t1, cprob)
    show()

def probabilitygraph(data, vec1, high, k=5, weightf=gaussian, ss=5.):
    t1 = arange(0., high, .1)
    probs = [probguess(data, vec1, v, v+.1, k, weightf) for v in t1]

    smoothed = []
    for i in range(len(probs)):
        sv = 0.
        for j in range(len(probs)):
            dist = abs(i-j)*.1
            weight = gaussian(dist, sigma=ss)
            sv += weight * probs[j]
        smoothed.append(sv)

    smoothed = array(smoothed)
    plot(t1, smoothed)
    show()

if __name__ == '__main__':
    import optimization as op
    data = wineset2()
    costf = createcostfunction(weightedknn, data)
    print op.genetic_optimize(weightdomain, costf, popsize=5, maxiter=20)
