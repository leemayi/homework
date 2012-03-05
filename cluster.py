import sys
import random
from math import sqrt


def read_file(fname=sys.stdin):
    def func(f):
        header = f.readline()
        col_names = header.rstrip().split('\t')[1:]

        row_names, data = [], []
        for line in f.xreadlines():
            cols = line.rstrip().split('\t')
            row_names.append(cols[0])
            data.append([float(x) for x in cols[1:]])
        return row_names, col_names, data

    if isinstance(fname, file):
        return func(fname)
    else:
        with open(fname) as f:
            return func(f)


def pearson(v1, v2):
    n = len(v1)
    sum1 = sum(v1)
    sum2 = sum(v2)
    sum1Sq = sum([x**2 for x in v1])
    sum2Sq = sum([x**2 for x in v2])
    pSum = sum([(v1[i]*v2[i]) for i in range(n)])

    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - sum1**2/n) * (sum2Sq - sum2**2/n))
    if den == 0:
        return 0
    return 1. - num/den

def tanimoto(v1, v2):
    c1, c2, shr = 0, 0, 0.
    for i in range(len(v1)):
        if v1[i] != 0:
            c1 += 1
        if v2[i] != 0:
            c2 += 1
        if v1[i] != 0 and v2[i] != 0:
            shr += 1
    if (c1+c2-shr) == 0:
        return 0
    return 1. - (shr/(c1+c2-shr))

def manhattan(v1, v2):
    d = 0.
    for i in range(len(v1)):
        d += abs(v1[i] - v2[i])
    return d


def kcluster(rows, distance=pearson, k=4):
    r, c = len(rows), len(rows[0])
    ranges = [ (min([row[i] for row in rows]),
                max([row[i] for row in rows]))
        for i in range(c) ]

    clusters = [[ (random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0])
        for i in range(c) ]
        for _ in range(k) ]

    last_matches = None
    for t in range(100):
        print 'Iteration', t
        best_matches = [[]]*k

        for j, row in enumerate(rows):
            best_match = 0
            best_dist = distance(clusters[best_match], row)
            for i in range(1, k):
                d = distance(clusters[i], row)
                if d < best_dist:
                    best_match = i
                    best_dist = d
            best_matches[best_match].append(j)

        if best_matches == last_matches:
            break
        last_matches = best_matches

        for i in range(k):
            avgs = [0.]*c
            for rid in best_matches[i]:
                for m in range(c):
                    avgs[m] += rows[rid][m]
            for m in range(c):
                avgs[m] /= len(best_matches[i])
            clusters[i] = avgs

    dist = [0.]*k
    for i in range(k):
        n = len(best_matches[i])
        for j in range(n):
            for m in range(j+1, n):
                dist[i] += distance(rows[best_matches[i][j]], rows[best_matches[i][m]])

    return best_matches, dist, clusters

def scale_down(data, distance=pearson, nd=2, rate=.01):

    def euclidean(p1, p2):
        return sqrt(sum([((p1[i]-p2[i])**2)
            for i in range(nd)]))

    n = len(data)
    real_dist = [[distance(data[i], data[j])
        for j in range(n)]
        for i in range(n)]

    loc = [[random.random() for _ in range(nd)] for _ in range(n)]

    last_error = None
    for m in range(10):
        fake_dist = [[euclidean(loc[i], loc[j])
            for j in range(n)]
            for i in range(n)]

        grad = [[0.]*nd for _ in range(n)]
        total_error = 0
        for i in range(n):
            for j in range(n):
                if i == j: continue
                error_term = (fake_dist[i][j]-real_dist[i][j])/real_dist[i][j]
                for k in range(nd):
                    grad[i][k] += (loc[i][k]-loc[j][k]) / fake_dist[i][j] * error_term
                total_error += abs(error_term)
        print total_error
        if last_error and last_error < total_error:
            break
        last_error = total_error

        for i in range(n):
            for k in range(nd):
                loc[i][k] -= rate*grad[i][k]
    return loc

def draw2d(data, labels, fname, coding='PNG'):
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (2000,2000), (255,255,255))
    draw = ImageDraw.Draw(img)
    for i in range(len(data)):
        x = (data[i][0] + .5) * 1000
        y = (data[i][1] + .5) * 1000
        draw.text((x,y), labels[i], (0,0,0))
    img.save(fname, coding)


def test_zebo():
    wants, people, data = read_file('data/zebo.txt')
    loc = scale_down(data, tanimoto)
    draw2d(loc, wants, 'zebo.png')
    

def test_blogs():
    blog_names, words, data = read_file('data/blogdata.txt')
    clust, dist, center = kcluster(data, k=10)
    print dist



if __name__ == '__main__':
    test_zebo()
