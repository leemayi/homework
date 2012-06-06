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


def logistic_cost_function(theta, X, y, lambda_=0):
    m = y.size
    o = sigmoid(np.dot(X, theta))
    J = (-1./m) * (np.dot(y.T, np.log(o)) + np.dot((1.-y).T, np.log(1.-o))) \
        + (lambda_/(2.*m)) * np.dot(theta[1:], theta[1:])
    return J


def logistic_grad_function(theta, X, y, lambda_=0):
    m = y.size
    o = sigmoid(np.dot(X, theta))
    grad = (1./m) * np.dot(X.T, o-y)
    grad[1:] += (lambda_/m) * theta[1:]
    return grad


class step(object):
    def __init__(self, n=1):
        self.i = 0
        self.n = n
    def __call__(self, xk):
        self.i += 1
        if self.i % self.n == 0:
            print 'Iteration %02d' % self.i


