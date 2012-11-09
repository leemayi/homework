import sys
from random import random
from svm import *


def sample(n=10):
    def f(x1, x2):
        return 32.3*x1 + 15.7*x2 + 8.2
    y = []
    node = []
    for _ in range(n):
        x1 = random() * 51 + 33
        x2 = random() * 24 + 13
        node.append((x1, x2))
        y.append(f(x1, x2))
    return (y, node)

def split(y, node, ratio=.3):
    n = int(len(y) * (1-ratio))
    return y[:n], node[:n], y[n:], node[n:]

if __name__ == '__main__':
    y, node = sample(int(sys.argv[1]))
    for i, (x1, x2) in enumerate(node):
        print '%f 1:%f 2:%f' % (y[i], x1, x2)
