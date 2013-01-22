from pylab import *
import numpy as np
from svmutil import *
svm_model.predict = lambda self, x: svm_predict([0], [x], self)[0][0]


def rpoints(center, sigma, count):
    mean = center
    cov = [[sigma, 0], [0, sigma]]
    return np.random.multivariate_normal(mean, cov, count)


def train():
    x1 = rpoints((0, 0), 1, 100)
    x2 = rpoints((4, 3), 1, 100)
    y = [1] * len(x1) + [0] * len(x2)
    x = [ list(pair) for pair in np.vstack((x1, x2)) ]

    prob = svm_problem(y, x)
    param = svm_parameter()
    param.kernel_type = RBF
    param.C = 10

    m = svm_train(prob, param)

    scatter(*x1.T, c='r', marker='x')
    scatter(*x2.T, c='b', marker='+')

    for xnew in rpoints((2, 3), 1, 10):
        xnew = list(xnew)
        py = m.predict(xnew)
        if py == 1:
            c = 'r'
        else:
            c = 'b'
        scatter(*xnew, c=c, marker='o')
    show()


train()
