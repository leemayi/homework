import os
import math
import struct

import scipy.io as io
from PIL import Image
import numpy as np

from util import ml_class_path


def display_data(X, example_width=None):
    if not example_width:
        example_width = int(math.sqrt(X.shape[1]))


def ex3():
    with open('train-images.idx3-ubyte', 'rb') as f:
        magic, nimages, nrows, ncols = struct.unpack('>4I', f.read(4*4))
        n = nrows * ncols
        print magic, nimages, nrows, ncols, n
        Image.fromstring('L', (nrows, ncols), f.read(n)).show()
    return
    input_layer_size = 400
    num_labels = 10

    vars = io.loadmat(os.path.join(ex3path, 'ex3data1.mat'))
    _X, y = np.array(vars['X'], dtype=np.uint8), vars['y']

    img = Image.fromarray(_X[1,:].reshape((20,20)), 'L')
    img.show()


if __name__ == '__main__':
    ex3path = os.path.join(ml_class_path(), 'ex3')
    ex3()