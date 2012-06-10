import sys
import unittest
from math import log

import numpy as np


TITLE, TOTAL = None, None

log2 = lambda x: log(x) / log(2)



class Node(object):

    def __init__(self, is_leaf, label=None, X=None, y=None):
        if is_leaf:
            self.make_leaf(X, y)
        else:
            self.make_node(label)

    def make_node(self, label):
        self.is_leaf = False
        self.label = label
        self.children = {}

    def make_leaf(self, X, y):
        self.is_leaf = True
        self.X = X
        self.y = y
        self.calc()
        self.label = self.make_label()
        if hasattr(self, 'children'):
            del self.children

    def add_child(self, label, child):
        self.children[label] = child

    def calc(self):
        self.size = self.y.shape[0]

        max_k, max_v = None, None
        for k, v in dist(self.y):
            if max_v is None or v > max_v:
                max_v = v
                max_k = k

        self.target = max_k
        self.dominant = max_v

    def make_label(self):
        return '%s:%d%%(%d%%) %s' % (
            self.target,
            self.dominant*100/self.size,
            self.size*100/TOTAL,
            ','.join(['%s:%d'%(k,v) for k,v in dist(self.y)]),
            )

    def __str__(self):
        return self.label


def dist(y):
    m = float(len(y))
    return [ (val, sum(y == val)) for val in set(y) ]


def entropy(y):
    m = float(len(y))
    return -sum([ (v/m * log2(v/m)) for k, v in dist(y) ])


def generate_tree(X, y, ex=[], theta1=0., theta2=0., indent=0):
    if len(y) <= theta1:
        return Node(is_leaf=True, X=X, y=y)

    m, n = X.shape
    cur_e = entropy(y)
    bestg = 0

    for feature in range(n):
        if feature in ex:
            continue

        col = X[:,feature]
        values = set(col)
        if len(values) <= 1:
            continue

        e = 0
        for val in values:
            idx = col == val
            e += float(sum(idx)) / m * entropy(y[idx])
        gain = cur_e - e
        if gain > bestg:
            bestg = gain
            bestf = feature

    if bestg <= theta2:
        return Node(is_leaf=True, X=X, y=y)

    n = Node(is_leaf=False, label=TITLE[bestf])

    for val, Xi, yi in split_by_feature(X, y, bestf):
        child = generate_tree(Xi, yi, ex+[bestf], theta1, theta2, indent+1)
        n.add_child(val, child)

    return n


def split_by_feature(X, y, feature):
    splits = []
    col = X[:,feature]

    for val in set(col):
        idx = col == val
        splits.append((val, X[idx], y[idx]))

    return splits


def dot(tree):
    def _print(t):
        if t.is_leaf:
            return
        for elabel, child in t.children.iteritems():
            print '  node%d [label="%s"];' % (id(t), t.label)
            print '  node%d [label="%s"];' % (id(child), child.label)
            print '  node%d -> node%d [label="%s"];' % (id(t), id(child), elabel)
            _print(child)

    print 'digraph {'
    _print(tree)
    print '}'


def prune_same_target(tree):
    if tree.is_leaf:
        return

    for child in tree.children.values():
        prune_same_target(child)

    leafs = filter(lambda i:i[1].is_leaf, tree.children.items())
    nodes = filter(lambda i:not i[1].is_leaf, tree.children.items())

    targets = set([ leaf.target for _,leaf in leafs ])
    if len(targets) > 1:
        return

    Xmerge = np.vstack(map(lambda i:i[1].X, leafs))
    ymerge = np.hstack(map(lambda i:i[1].y, leafs))
    if nodes:
        ELSE = Node(is_leaf=True, X=Xmerge, y=ymerge)
        tree.children = dict([('ELSE', ELSE)] + nodes)
    else:
        tree.make_leaf(Xmerge, ymerge)


def prune_small_branches(tree, threshold):
    if not hasattr(tree, 'children'):
        return

    for child in tree.children.values():
        prune_small_branches(child, threshold)

    leafs = filter(lambda i:i[1].is_leaf, tree.children.items())
    nodes = filter(lambda i:not i[1].is_leaf, tree.children.items())

    if not leafs:
        return

    leafs.sort(lambda i,j: cmp(i[1].size, j[1].size))

    s, idx = 0, 0
    for _, leaf in leafs:
        s += leaf.size
        if s > threshold:
            break
        idx += 1
    if idx < 1:
        return

    Xmerge = np.vstack(map(lambda i:i[1].X, leafs[:idx]))
    ymerge = np.hstack(map(lambda i:i[1].y, leafs[:idx]))
    if nodes or leafs[idx:]:
        ELSE = Node(is_leaf=True, X=Xmerge, y=ymerge)
        tree.children = dict([('ELSE', ELSE)] + leafs[idx:] + nodes)
    else:
        tree.make_leaf(Xmerge, ymerge)



def test():
    global TITLE, TOTAL
    data = np.array([line.rstrip().split() \
        for line in open('data/play_tennis.data')])
    TITLE = data[0,1:] 
    X, y = data[1:,1:-1], data[1:,-1]
    TOTAL = len(y)

    tree = generate_tree(X, y)
    dot(tree)


def main():
    global TITLE, TOTAL
    data = np.array([line.rstrip().split('\t') \
                     for line in open('data/pay_cleaned.log')])
    TITLE = data[0,:]
    X, y = data[1:,:-1], data[1:,-1]
    TOTAL = len(y)
    
    tree = generate_tree(X, y, theta1=TOTAL*.05)
    #prune_small_branches(tree, TOTAL*.1)
    #prune_same_target(tree)
    dot(tree)


if __name__ == '__main__':
    test()
