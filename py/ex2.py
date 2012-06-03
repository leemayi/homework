import os

import numpy as np
import pylab as pl
import scipy.optimize as opt

from util import ml_class_path, load_txt, sigmoid, gd
from ex1 import feature_normalize


def plot_data(X, y):
    pl.figure()
    pl.plot(X[y==1,0], X[y==1,1], 'k+')
    pl.plot(X[y==0,0], X[y==0,1], 'ko')
    

def cost_function(theta, X, y, lambda_=0):
    m = y.size
    n = theta.size

    o = sigmoid(np.dot(X, theta))

    J = (-1./m) * (np.dot(y.T, np.log(o)) + np.dot((1.-y).T, np.log(1.-o))) \
        + (lambda_/(2.*m)) * np.dot(theta[1:], theta[1:])

    grad = (1./m) * np.dot(X.T, o-y)
    grad[1:] += (lambda_/m) * theta[1:]

    return J, grad


def plot_decision_boundary(theta, X, y):
    plot_data(X[:,1:], y)
    
    plot_x = np.arange(X[:,1].min()-2, X[:,1].max()+2)
    plot_y = (-1. / theta[2]) * (theta[1] * plot_x + theta[0])

    pl.plot(plot_x, plot_y)
    pl.axis([X[:,1].min()-.1,
             X[:,1].max()+.1,
             X[:,2].min()-.1,
             X[:,2].max()+.1,
             ])


def ex2():
    data = load_txt(os.path.join(ex2path, 'ex2data1.txt'))
    _X = data[:,:2]
    y = data[:,2]

    plot_data(_X, y)
    pl.xlabel('Exam 1 score')
    pl.ylabel('Exam 2 score')
    pl.legend(('Admitted', 'Not admitted'))

    # compute cost and gradient
    m, n = _X.shape
    X = np.hstack((np.ones((m, 1)), _X))

    initial_theta = np.zeros(n+1)

    cost, grad = cost_function(initial_theta, X, y)
    print 'cost at initial theta (zeros):', cost
    print 'gradient at initial theta (zeros):', grad

    #optimizing using gradient descent
    X_norm, mu, sigma = feature_normalize(_X)
    X = np.hstack((np.ones((m, 1)), X_norm))
    theta, Jhist = gd(cost_function, X, y, initial_theta, alpha=5, maxiter=200)
    print 'gd: theta:', theta, 'cost:', cost_function(theta, X, y)[0]

    pl.plot(Jhist)
    plot_decision_boundary(theta, X, y)

    #optimizing using scipy.optimize
    X = np.hstack((np.ones((m, 1)), _X))

    def costf(theta):
        return cost_function(theta, X, y)[0]

    def difff(theta):
        return cost_function(theta, X, y)[1]

    print opt.check_grad(costf, difff, initial_theta)

    #TODO: fmin_cg does't work here, why? what's the difference?
    theta, allvec = opt.fmin_ncg(costf, initial_theta, difff, retall=1)
    print 'fmin_cg: theta:', theta, 'cost:', cost_function(theta, X, y)[0]
    Jhist = [costf(t) for t in allvec]

    pl.plot(Jhist)
    plot_decision_boundary(theta, X, y)


def ex2_reg():
    data = load_txt(os.path.join(ex2path, 'ex2data2.txt'))
    _X = data[:,:2]
    y = data[:,2]

    plot_data(_X, y)
    pl.xlabel('Microchip Test 1')
    pl.ylabel('Microchip Test 2')
    pl.legend(['y=1', 'y=0'])




if __name__ == '__main__':
    ex2path = os.path.join(ml_class_path(), 'ex2')
    ex2_reg()
    pl.show()

