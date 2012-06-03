import os

import numpy as np
import pylab as pl
import scipy.optimize as opt

from util import ml_class_path, load_txt, sigmoid, gd
from ex1 import feature_normalize


def plot_data(X, y):
    false = (np.zeros(y.shape) == 1)
    pl.figure()
    pl.plot(X[np.hstack((y==1, false))],
        X[np.hstack((false, y==1))], 'k+')
    pl.plot(X[np.hstack((y==0, false))],
        X[np.hstack((false, y==0))], 'ko')
    pl.xlabel('Exam 1 score')
    pl.ylabel('Exam 2 score')
    pl.legend(('Admitted', 'Not admitted'))
    

def cost_function(theta, X, y, lambda_=0):
    m = y.size
    n = theta.size

    print '-'*10
    print '#0'
    print X.shape, theta.shape
    #print X * theta
    print '#1'

    J = (-1./m) * (y.T * np.log(sigmoid(X*theta)) + (1.-y).T * np.log(1.-sigmoid(X*theta)))[0,0] \
        + (lambda_/(2.*m)) * np.multiply(theta[1:], theta[1:]).sum()
    print '#2'
    grad = (1./m) * X.T * (sigmoid(X*theta) - y)
    print '#3'
    grad[1:] += (lambda_/m) * theta[1:]
    print '#4'
    theta.flatten()
    print J
    print grad.shape
    print grad

    return J, grad.flatten()


def plot_decision_boundary(theta, X, y):
    plot_data(X[:,1:], y)
    
    plot_x = np.arange(X[:,1].min()-2, X[:1].max()+2)
    plot_y = (-1. / theta[2,0]) * (theta[1,0] * plot_x + theta[0,0])

    pl.plot(plot_x, plot_y)
    pl.axis([X[:,1].min()-.1,
             X[:,1].max()+.1,
             X[:,2].min()-.1,
             X[:,2].max()+.1,
             ])


def ex2():
    data = load_txt(os.path.join(ex2path, 'ex2data1.txt'))
    _X = data[:, :2]
    y = data[:, 2]

    #plot_data(_X, y)
    #pl.show()

    # compute cost and gradient
    m, n = _X.shape
    X = np.hstack((np.ones((m, 1)), _X))

    initial_theta = np.zeros((n+1, 1))

    '''
    cost, grad = cost_function(initial_theta, X, y)
    print 'cost at initial theta (zeros):', cost
    print 'gradient at initial theta (zeros):', grad
    '''

    #optimizing using gradient descent
    '''
    X_norm, mu, sigma = feature_normalize(_X)
    X = np.hstack((np.ones((m, 1)), X_norm))
    theta, Jhist = gd(cost_function, X, y, initial_theta, alpha=5, maxiter=200)
    print 'gd: theta:', theta, 'cost:', cost_function(theta, X, y)[0]

    pl.plot(Jhist)
    plot_decision_boundary(theta, X, y)
    pl.show()
    '''

    #optimizing using scipy.optimize
    X = np.hstack((np.ones((m, 1)), _X))

    def costf(theta):
        return cost_function(theta, X, y)[0]

    def difff(theta):
        return cost_function(theta, X, y)[1]

    theta, Jhist = opt.fmin_cg(costf, initial_theta, difff, retall=1)
    print 'fmin_cg: theta:', theta, 'cost:', cost_function(theta, X, y)[0]

    pl.plot(Jhist)
    plot_decision_boundary(theta, X, y)
    pl.show()


if __name__ == '__main__':
    ex2path = os.path.join(ml_class_path(), 'ex2')
    ex2()

