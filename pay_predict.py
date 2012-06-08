import sys
from math import log
import unittest
import numpy as np

log2 = lambda x: log(x) / log(2)


class Node(object):

    def __init__(self, label, children={}):
        self.label = str(label)
        self.children = children

    def add_child(self, label, child):
        self.children[label] = child


class Leaf(object):

    def __init__(self, X, y):
        self.label = self.make_label(X, y)

    def make_label(self, X, y):
        m = y.shape[0]
        max_k, max_v = None, None
        for k, v in dist(y):
            if max_v is None or v > max_v:
                max_v = v
                max_k = k
        return '%s: %d%% %d%%' % (max_k, max_v*100/m, m*100/TOTAL)


def dist(y):
    m = float(len(y))
    return [ (val, (sum(y == val) / m)) for val in set(y) ]


def entropy(y):
    m = float(len(y))
    return -sum([ (v/m * log2(v/m)) for k, v in dist(y) ])


def generate_tree(X, y, ex=[], theta1=0., theta2=0.):
    if len(y) <= theta1:
        return Node('nil')

    m, n = X.shape
    cur_e = entropy(y)
    min_e = float(sys.maxint)

    for feature in range(n):
        if feature in ex:
            continue

        col = X[:,feature]
        e = 0
        for val in set(col):
            idx = col == val
            e -= float(sum(idx)) / m * entropy(y[idx])

        if e < min_e:
            min_e = e
            bestf = feature

    gain = cur_e - min_e
    if gain <= theta2:
        return Leaf(X, y)

    n = Node(str(bestf))

    for val, Xi, yi in split_by_feature(X, y, bestf):
        child = generate_tree(Xi, yi, ex+[bestf], theta1, theta2)
        n.add_child(val, child)

    return n


def split_by_feature(X, y, feature):
    splits = []
    col = X[:,feature]

    for val in set(col):
        idx = col == val
        splits.append((val, X[idx], y[idx]))

    return splits


class EntroyTest(unittest.TestCase):

    def test_1(self):
        self.assertEquals(0, entropy(np.zeros(2)))

    def test_2(self):
        self.assertEquals(1, entropy(np.array([0, 1])))

    def test_4(self):
        self.assertEquals(2, entropy(np.array([0, 1, 2, 3])))

    def test_9_1(self):
        self.assertEquals(-.9*log2(.9)-.1*log2(.1),
                          entropy(np.array([0]*9+[1])))



if __name__ == '__main__':
    data = np.array([line.rstrip().split('\t') \
                     for line in open('data/pay_cleaned.log')])
    X, y = data[:,:-1], data[:,-1]
    TOTAL = len(y)
    
    tree = generate_tree(X, y)



def classify(observation, tree):
    if tree.results != None:
        return tree.results
    v = observation[tree.col]
    branch = None
    if isinstance(v, int) or isinstance(v, float):
        if v >= tree.value:
            branch = tree.tb
        else:
            branch = tree.fb
    else:
        if v == tree.value:
            branch = tree.tb
        else:
            branch = tree.fb
    return classify(observation, branch)


def prune(tree, mingain):
    if tree.tb.results == None:
        prune(tree.tb, mingain)
    if tree.fb.results == None:
        prune(tree.fb, mingain)

    if tree.tb.results != None and tree.fb.results != None:
        tb, fb = [], []
        for v, c in tree.tb.results.items():
            tb += [[v]] * c
        for v, c in tree.fb.results.items():
            fb += [[v]] * c
        delta = entropy(tb + fb) - (entropy(tb) + entropy(fb)) / 2
        if delta < mingain:
            tree.tb, tree.fb = None, None
            tree.results = uniquecounts(tb + fb)


def prune2(tree, mincount):
    if tree.tb.results == None:
        prune2(tree.tb, mincount)
    if tree.fb.results == None:
        prune2(tree.fb, mincount)

    if tree.tb.results != None and tree.fb.results != None:
        cnt = sum(tree.tb.results.values()) + sum(tree.fb.results.values())
        if float(cnt) / total < mincount:
            tb, fb = [], []
            for v, c in tree.tb.results.items():
                tb += [[v]] * c
            for v, c in tree.fb.results.items():
                fb += [[v]] * c
            tree.tb, tree.fb = None, None
            tree.results = uniquecounts(tb + fb)


'''

if __name__ == '__main__':
    my_data = [line.rstrip().split('\t') for line in open('data/pay_cleaned.log')]
    total = len(my_data)
    tree = buildtree(my_data)
    prune(tree, .05)
    prune2(tree, .05)
    printtree(tree)
    drawtree(tree, 'treeview.png')

    sys.exit(0)
    printtree(tree)

    prune(tree, 1.)
    printtree(tree)


'''
