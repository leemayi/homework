import os

import numpy as np
import pylab as pl

from ex1 import ml_class_path, load_txt


def plot_data(X, y):
    pl.figure()
    pl.plot(X[np.array(y)==1, 0], X[y==1, 1], 'k+')
    pl.plot(X[y==0, 0], X[y==0, 1], 'ko')
    pl.show()
    

def ex2():
    data = load_txt(os.path.join(ex2path, 'ex2data1.txt'))
    _X = data[:, :2]
    y = data[:, 2]

    plot_data(_X, y)



if __name__ == '__main__':
    ex2path = os.path.join(ml_class_path(), 'ex2')
    ex2()

