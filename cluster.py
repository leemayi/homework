import random
from math import sqrt


def read_file(fname):
    with open(fname) as f:
        header = f.readline()
        col_names = header.rstrip().split('\t')[1:]

        row_names, data = [], []
        for line in f.xreadlines():
            cols = line.rstrip().split('\t')
            row_names.append(cols[0])
            data.append([float(x) for x in cols[1:]])
    return row_names, col_names, data


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
        if v2[i] != 0 and v2[i] != 0:
            shr += 1
    return 1. - (shr/c1+c2-shr)

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

    return best_matches


def test_zebo():
    wants, people, data = read_file('data/zebo.txt')

def test_blogs():
    blog_names, words, data = read_file('data/blogdata.txt')
    print len(blog_names), len(words), len(data), len(data[0])
    clust = kcluster(data, k=10)


if __name__ == '__main__':
    test_blogs()
