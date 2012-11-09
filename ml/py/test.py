import pylab as pl
import numpy as np


x = np.linspace(-1, 1, 50)
y = np.linspace(-1, 1, 50)
z = np.zeros((x.size, y.size))

for i in range(x.size):
    for j in range(y.size):
        t = 1 - np.square(x[i]) - np.square(y[j])
        if t > 0:
            z[i,j] = np.sqrt(t)

pl.contour(z, [0, 0])
pl.show()