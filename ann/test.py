import sys
import numpy as np
import neurolab as nl


net = nl.net.newff([(0,255)]*400, [25, 10])
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

error = nl.train.train_gd(net, X, y, epochs=50, show=1, lr=100)
print 'error:', error

out = net.sim(X)
print 'accuracy:', float((out == y).sum()) / y.size
