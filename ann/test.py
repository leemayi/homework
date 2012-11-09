import sys
import numpy as np
import neurolab as nl
import pylab as pl



def build_net():
    net = nl.net.newff([(0,255)]*400, [25, 10], [nl.trans.LogSig()]*2)
    print 'ci:', net.ci
    print 'co:', net.co
    print 'layers:', len(net.layers)

    X = np.load('data/X.npy')
    y_orig = np.load('data/y.npy')
    print 'X:', X.shape
    print 'y:', y_orig.shape

    y = np.zeros((y_orig.shape[0], 10))
    for i, yi in enumerate(y_orig):
        idx = 0 if yi[0] == 10 else yi[0]
        y[i,idx] = 1 

    print y.shape
    print y_orig
    print y

    error = nl.train.train_ncg(net, X, y, epochs=50, show=1)
    #cost function is different

    pl.plot(error)
    pl.xlabel('iteration')
    pl.ylabel('error')
    pl.show()


    out = net.sim(X)
    def maxi(vec):
        maxi = 0
        maxv = vec[maxi]
        for i,v in enumerate(vec):
            if v > maxv:
                maxv = v
                maxi = i
        return maxi
    for i in range(5):
        print out[i], y_orig[i], maxi(out[i])
    print 'accuracy:', float((out == y).sum()) / y.size
    #net.save('net.data')

build_net()
