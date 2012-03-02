import sys
import random
from math import sqrt

import numpy as np
from PIL import Image, ImageDraw


def read_file(filename):
    fp = open(filename)
    line = fp.readline()

    colnames = line.rstrip().split('\t')[1:]
    rownames = []
    data = []

    for line in fp.xreadlines():
        p = line.rstrip().split('\t')
        rownames.append(p[0])
        
        data.append([float(x) for x in p[1:]])

    return np.array(rownames), np.array(colnames), np.array(data)

def pearson(v1, v2):
    n = v1.size
    sum1 = sum(v1)
    sum2 = sum(v2)

    num = sum(v1*v2) - (sum1 * sum2 / n)
    den = sqrt((sum(v1**2) - sum1**2 / n) * (sum(v2**2) - sum2**2 / n))
    if den == 0:
        return 0
    return 1.0 - num / den

def tanimoto(v1, v2):
    vv1, vv2 = v1.astype(bool).astype(int), v2.astype(bool).astype(int)
    c1 = sum(vv1)
    c2 = sum(vv2)
    shr = sum(vv1 & vv2)
    return 1.0 - (float(shr)/(c1+c2-shr))

class Bicluster(object):

    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.vec = vec
        self.left = left
        self.right = right
        self.id = id
        self.distance = distance

def hcluster(rows, distance=pearson):
    assert rows
    distances = {}
    currentclustid = -1

    clust = [ Bicluster(row, id=i) for i, row in enumerate(rows) ]
    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        n = len(clust)
        for i in range(n):
            for j in range(i+1, n):
                pair = (clust[i].id, clust[j].id)
                if pair not in distances:
                    d = distance(clust[i].vec, clust[j].vec)
                    distances[pair] = d
                else:
                    d = distances[pair]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        i, j = lowestpair
        c1, c2 = clust[i], clust[j]
        v1, v2 = c1.vec, c2.vec
        mergevec = [ ((v1[k] + v2[k] ) / 2.0) for k in range(len(v1)) ]

        newcluster = Bicluster(mergevec,
            left=c1, right=c2,
            distance=closest, id=currentclustid)

        currentclustid -= 1
        try:
            del clust[j]
            del clust[i]
        except IndexError:
            print '#1', len(clust), i, j
            print lowestpair
            raise
        clust.append(newcluster)

    return clust[0]

def draw_dendrogram(clust, labels, fname='clusters.png', encoder='PNG'):

    def get_height(clust):
        if clust.left is None and clust.right is None:
            return 1
        return get_height(clust.left) + get_height(clust.right)

    def get_depth(clust):
        if clust.left is None and clust.right is None:
            return 0
        return max(get_depth(clust.left), get_depth(clust.right))+clust.distance

    def draw_node(draw, clust, x, y, scaling, lables):
        if clust.id < 0:
            h1 = get_height(clust.left) * 20
            h2 = get_height(clust.right) * 20
            top = y - (h1 + h2) /2
            bottom = y + (h1 + h2) / 2
            ll = clust.distance * scaling
            draw.line((x, top+h1/2, x, bottom-h2/2), fill=(255,0,0))
            draw.line((x, top+h1/2, x+ll, top+h1/2), fill=(255,0,0))
            draw.line((x, bottom-h2/2, x+ll, bottom-h2/2), fill=(255,0,0))
            draw_node(draw, clust.left, x+ll, top+h1/2, scaling, labels)
            draw_node(draw, clust.right, x+ll, bottom-h2/2, scaling, labels)
        else:
            draw.text((x+5,y-7), labels[clust.id], (0,0,0))

    h = get_height(clust)*20
    w = 1200
    depth = get_depth(clust)

    scaling = float(w-150)/depth

    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h/2, 10, h/2), fill=(255, 0, 0))
    draw_node(draw, clust, 10, h/2, scaling, labels)
    img.save(fname, encoder)

def rotate_matrix(data):
    newdata = []
    r = len(data)
    c = len(data[0])
    newdata = [[ data[j][i] for j in range(r) ] for i in range(c) ]
    return newdata

def kcluster(rows, distance=pearson, k=4):
    r, c = rows.shape
    ranges = [ (min(rows[:,i]), max(rows[:,i])) for i in range(c) ]

    clusters = [[(random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0])
        for i in range(len(rows[0]))] for _ in range(k)]

    lastmatches = None
    for t in range(100):
        print 'Iteration', t
        bestmatches = [[]] * k

        for j, row in enumerate(rows):
            bestmatch = 0
            bestmatch_distance = distance(clusters[bestmatch], row)
            for i in range(k):
                d = distance(clusters[i], row)
                if d < bestmatch_distance:
                    bestmatch = i
                    bestmatch_distance = d
            bestmatches[bestmatch].append(j)

        if bestmatches == lastmatches:
            break
        lastmatches = bestmatches

        for i in range(k):
            avgs = [0.] * len(rows[0])
            if len(bestmatches[i]) > 0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(bestmatches[i])
                clusters[i] = avgs

    return bestmatches

def scale_down(data, distance=pearson, rate=.01):
    n = len(data)

    realdist = [[distance(data[i],data[j]) for j in range(n)]
        for i in range(n)]

    outersum = 0.
    loc = [[random.random(), random.random()] for i in range(n) ]
    fakedist = [[0]*n]*n

    lasterror = None
    for _ in range(1000):
        for i in range(n):
            for j in range(n):
                fakedist[i][j] = sqrt(sum([pow(loc[i][x]-loc[j][x], 2)
                    for x in range(len(loc[i]))]))

        grad = [[0., 0.]]*n
        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k:
                    continue
                errorterm = (fakedist[j][k]-realdist[j][k])/realdist[j][k]

                grad[k][0] += ((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm
                grad[k][1] += ((loc[k][1]-loc[j][1])/fakedist[j][k])*errorterm

                totalerror += abs(errorterm)
        print totalerror

        if lasterror and lasterror < totalerror:
            break
        lasterror = totalerror

        for k in range(n):
            loc[k][0] -= rate*grad[k][0]
            loc[k][1] -= rate*grad[k][1]

    return loc

def draw2d(data, lables, fname='mds2d.png', encoder='PNG'):
    img = Image.new('RGB', (2000,2000), (255,255,255))
    draw = ImageDraw.Draw(img)
    for i in range(len(data)):
        x = (data[i][0]+.5)*1000
        y = (data[i][1]+.5)*1000
        draw.text((x,y), lables[i], (0,0,0))
    img.save(fname, encoder)



def test_hcluster():
    blognames, words, data = read_file('blogdata.txt')
    clust = hcluster(data)
    draw_dendrogram(clust, blognames, fname='blogclust.png')

    rdata = rotate_matrix(data)
    wordclust = hcluster(rdata)
    draw_dendrogram(wordclust, words, fname='wordclust.png')

def test_kcluster():
    blognames, words, data = read_file('blogdata.txt')
    def p(clust, lables):
        print ' '.join([lables[r] for r in clust])

    kclust = kcluster(data, k=10)
    p(kclust[0], blognames)

    rdata = rotate_matrix(data)
    wordclust = kcluster(data, k=30)
    p(wordclust[0], words)
    
def test_zebo():
    wants, people, data = read_file('zebo.txt')
    clust = hcluster(data, distance=tanimoto)
    draw_dendrogram(clust, wants, 'wants.png')

def test_draw2d():
    wants, people, data = read_file('zebo.txt')
    coords = scale_down(data, tanimoto)
    draw2d(coords, wants)
    
    


if __name__ == '__main__':
    blognames, words, data = read_file('blogdata.txt')
    print data.shape
    print np.ptp(data[:,0])
    
