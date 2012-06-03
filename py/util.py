import os

import numpy as np


def ml_class_path():
    fpath = os.path.realpath(__file__)
    pos = fpath.find('ml-class')
    assert pos >= 0
    return fpath[:pos+len('ml-class')]


def load_txt(fname):
    with open(fname) as f:
        return np.array([ map(float, line.rstrip().split(',')) \
            for line in f.xreadlines() ])


def sigmoid(z):
    return 1. / (1. + np.exp(-z))


def sigmoidGradient(z):
    return np.multiply(sigmoid(z), 1-sigmoid(z))


def gd(cost_function, X, y, theta, alpha=.01, maxiter=50):
    J_history = np.zeros(maxiter)

    for i in range(maxiter):
        cost, grad = cost_function(theta, X, y)
        theta -= (alpha * grad)
        J_history[i] = cost

    return theta, J_history
