import os
import math
import struct

import scipy.io as io
import scipy.optimize as opt
from PIL import Image
import numpy as np
import pylab as pl


from util import ml_class_path, sigmoid, logistic_cost_function, logistic_grad_function, step


def display_data(X, example_width=None):
    if not example_width:
        example_width = int(math.sqrt(X.shape[1]))


def load_image():
    with open('train-images.idx3-ubyte', 'rb') as f:
        magic, nimages, nrows, ncols = struct.unpack('>4I', f.read(4*4))
        n = nrows * ncols
        print magic, nimages, nrows, ncols, n
        Image.fromstring('L', (nrows, ncols), f.read(n)).show()


def make_grid(X, size, grid_row=10, grid_col=10):
    grid = np.vstack([ np.hstack([ X[i+j,:].reshape(size) for j in range(grid_col) ]) \
        for i in range(0, min(X.shape[0], grid_row*grid_col), grid_col) ])
    print grid.shape

    return Image.fromarray(grid, 'L')




def one_vs_all(_X, y, num_labels, lambda_):
    m, n = _X.shape
    X = np.hstack((np.ones((m, 1)), _X))

    all_theta = []
    for c in range(num_labels):
        if c == 0: c = 10
        
        def costf(theta):
            return logistic_cost_function(theta, X, y==c, lambda_)
        def gradf(theta):
            return logistic_grad_function(theta, X, y==c, lambda_)

        maxiter = 50
        initial_theta = np.zeros(n+1)
        theta, allvec = opt.fmin_ncg(costf, initial_theta, gradf, maxiter=maxiter, retall=1, callback=step())
#        Jhist = map(costf, allvec)
#        pl.plot(Jhist)
#        pl.show()
        all_theta.append(theta)
    return np.vstack(all_theta)


def max_index(v):
    max_idx = 0
    max_ = v[0]
    for i in range(v.size):
        if v[i] > max_:
            max_ = v[i]
            max_ix = i
    return max_idx


def predict_one_vs_all(all_theta, _X):
    m = _X.shape[0]
    X = np.hstack((np.ones((m, 1)), _X))
    
    theta0 = all_theta[0]
    p = sigmoid(np.dot(X, theta0))
    print p.shape
    print p
    
    p = np.dot(X, all_theta.T)
    return np.array(map(max_index, p))


def ex3():
    input_layer_size = 400
    num_labels = 10

    vars = io.loadmat(os.path.join(ex3path, 'ex3data1.mat'))
    _X, y = np.array(vars['X']*128+128, dtype=np.ubyte), vars['y'].reshape(vars['y'].size)
    size = (math.sqrt(_X.shape[1]), math.sqrt(_X.shape[1]))

    #FIXME: image loading seems not fully correct
    #img = make_grid(np.random.permutation(_X)[:400,:], size, 20, 20)
    #img.show()

    print 'Training One-vs-All Logistic Regression'
    lambda_ = 1.
    all_theta = one_vs_all(_X, y, num_labels, lambda_)
    p = predict_one_vs_all(all_theta, _X)
    print 'Training Set Accuracy:', (p == y).mean() * 100


if __name__ == '__main__':
    ex3path = os.path.join(ml_class_path(), 'ex3')
    ex3()