from math import log
import numpy as np


def load(fname):

    def readn(fp, start_or_stop, stop=None):
        if stop is None:
            start, stop = 0, start_or_stop
        else:
            start, stop = start_or_stop, stop
        assert start < stop

        for _ in xrange(n):
            yield fp.readline()

    with open(fname) as f:
        meta = {}
        for line in head(f, 5):
            if line.startswith('#') and ':' in line:
                key, val = line[1:].split(':', 1)
                meta[key.strip()] = val.strip()
        return meta


print load('X.txt')


def ex4():
    input_layer_size = 400
    hidden_layer_size = 25
    num_lables = 10

    pass


def nnCostFunction(theta1,
    theta2,
    input_layer_size,
    hidden_layer_size,
    num_labels,
    X,
    y,
    lambda_):
    '''
    the neural network cost function for a two layer neural network
    J, grad = nnCostFunction(...)
    '''
    m = X.shape[0]
    J = 0
    theta1_grad = np.zeros(theta1.shape)
    theta2_grad = np.zeros(theta2.shape)

    for i in range(m):
        a1 = np.vstack(([1], X[i,:].T))

        z2 = theta1 * a1
        a2 = np.vstack(([1], sigmoid(z2)))

        z3 = theta2 * a2
        a3 = sigmoid(z3)

        h = a3

        yi = np.zeros((num_lables, 1))
        yi[y[i]] = 1

        J -= (yi.T * log(h) + (1-yi).T * log(1-h))

        d3 = a3 - yi

        d2 = (theta2.T * d3)[1:] * sigmoidGradient(z2)

        theta1_grad += d2 * a1.T
        theta2_grad += d3 * a2.T

    J += .5 * lambda_ * (sum(sum(theta1[:,1:] ** 2)) + sum(sum(theta2[:,1:] ** 2)))
    J /= m

    theta1_grad = (theta1_grad + np.hstack((np.zeros((theta1.shape[0], 1)), lambda_ * theta1[:,1:]))) / m
    theta2_grad = (theta2_grad + np.hstack((np.zeros((theta2.shape[0], 1)), lambda_ * theta2[:,1:]))) / m

    return J, (theta1_grad, theta2_grad)

