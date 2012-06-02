import os

import numpy as np
import pylab as pl
import scipy.linalg as linalg



def ml_class_path():
    fpath = os.path.realpath(__file__)
    pos = fpath.find('ml-class')
    assert pos >= 0
    return fpath[:pos+len('ml-class')]


def load_txt(fname):
    with open(fname) as f:
        return np.matrix([ map(float, line.rstrip().split(',')) \
            for line in f.xreadlines() ])


def plot_data(x, y):
    pl.plot(x, y, 'rx')
    pl.xlabel('x')
    pl.ylabel('y')


def compute_cost(X, y, theta):
    m = y.size
    J = np.square(X * theta - y).sum() / (2. * m)
    return J


def gradient_descent(X, y, theta, alpha, num_iters):
    m = y.size
    J_history = np.zeros((num_iters, 1))

    for i in range(num_iters):
        theta -= (alpha / m) * X.T * (X * theta - y)
        J_history[i] = compute_cost(X, y, theta)

    return theta, J_history


def ex1():
    data = load_txt(os.path.join(ex1path, 'ex1data1.txt'))
    _X = data[:,0]
    y = data[:,1]
    m = _X.size

    # Ploting
    plot_data(_X, y)

    # Gradient descent
    X = np.hstack((np.ones((m, 1)), _X))
    theta = np.zeros((2, 1))

    iterations = 1500
    alpha = 0.01

    print compute_cost(X, y, theta)

    theta, J_history = gradient_descent(X, y, theta, alpha, iterations)

    print 'Theta found by gradient descent: ', theta
    pl.plot(X[:,1], X*theta, '-')

    pl.figure()
    pl.plot(J_history)
    pl.show()


def feature_normalize(X):
    n = X.shape[1]

    X_norm = X[:]
    mu = np.zeros(n)
    sigma = np.zeros(n)

    for i in range(n):
        feature = X_norm[:,i]
        mu[i] = np.mean(feature)
        sigma[i] = np.std(feature)
        X_norm[:,i] -= mu[i]
        X_norm[:,i] /= sigma[i]

    return X_norm, mu, sigma


def normal_eqn(X, y):
    return linalg.pinv(X.T * X) * X.T * y


def ex1_multi():
    data = load_txt(os.path.join(ex1path, 'ex1data2.txt'))
    _X = data[:, :2]
    y = data[:, 2]
    m = y.size

    print 'First 10 examples from the dataset:'
    for i in range(10):
        print ' x = %s, y = %s' % (_X[i,:], y[i])
    print

    print 'Normalizing Features ...'
    X_norm, mu, sigma = feature_normalize(_X)

    X = np.hstack((np.ones((m, 1)), X_norm))

    print 'Running gradient descent ...'
    alpha = 1.
    num_iters = 400

    theta = np.zeros((3, 1))
    theta, J_history = gradient_descent(X, y, theta, alpha, num_iters)

    pl.figure()
    pl.plot(J_history, '-b')
    pl.xlabel('number of iterations')
    pl.ylabel('cost J')
    pl.show()

    print 'Theta computed from gradient descent:', theta

    a = (1650 - mu[0]) / sigma[0]
    b = (3 - mu[1]) / sigma[1]

    price = np.matrix([1, a, b]) * theta
    print 'Predicted price of a 1650 sq-ft, 3 br house',\
        '(using gradient descent):', price

    # Normal Equations
    data = load_txt(os.path.join(ex1path, 'ex1data2.txt'))
    _X = data[:, :2]
    y = data[:, 2]
    
    X = np.hstack((np.ones((m, 1)), _X))

    theta = normal_eqn(X, y)

    print 'Theta computed from the normal equations:', theta

    price = np.matrix('1 1650 3') * theta
    print 'Predicted price of a 1650 sq-ft, 3 br house',\
        '(using normal equations):', price


if __name__ == '__main__':
    ex1path = os.path.join(ml_class_path(), 'ex1')
    ex1_multi()
