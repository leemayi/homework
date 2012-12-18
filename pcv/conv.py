import sys
import math
from PIL import Image
import numpy as np
from scipy.ndimage import filters
from imtools import *
from utils import *


def kernel(sigma):
    sd = float(sigma)
    lw = int(4.0 * sd + 0.5)
    weights = [0.0] * (2 * lw + 1)
    weights[lw] = 1.0
    sum = 1.0
    sd = sd * sd
    # calculate the kernel:
    for ii in range(1, lw + 1):
        tmp = math.exp(-0.5 * float(ii * ii) / sd)
        weights[lw + ii] = tmp
        weights[lw - ii] = tmp
        sum += 2.0 * tmp
    for ii in range(2 * lw + 1):
        weights[ii] /= sum
    return weights

def show_weights(weights):
    l = len(weights)
    print l
    for i, w in enumerate(weights):
        if i == l/2:
            print '[%.2g]' % w,
        else:
            print '%.2g' % w,
    print

def _make_output(input):
    return np.zeros(input.shape)

def _conv_line(input, weights, output):
    lw = (len(weights) - 1) / 2
    la = len(input)
    for i in range(la):
        sum = 0.
        for j in range(i-lw, i+lw+1):
            if j >= 0 and j < la:
                sum += input[j] * weights[j-i+lw]
        output[i] = sum

def convolution(im, weights, axis=0, output=None):
    if output:
        im2 = output
    else:
        im2 = _make_output(im)

    for i in range(im.shape[axis]):
        if axis == 0:
            _conv_line(im[i,:], weights, im2[i,:])
        else:
            _conv_line(im[:,i], weights, im2[:,i])
    return im2

def my_gaussian_filter1d(input, sigma, axis=0):
    weights = kernel(sigma)
    return convolution(im, weights, axis)

def my_gaussian_filter(input, sigma):
    weights = kernel(sigma)
    im = convolution(input, weights, 0)
    return convolution(im, weights, 1)

def main():
    img = Image.open('data/empire.jpg').convert('L')
    im = array(img)

    sigma = 3
    im2 = my_gaussian_filter(im, sigma)
    im3 = filters.gaussian_filter(im, sigma)

    grid([img, toimg(im2), toimg(im3)]).show()



if __name__ == '__main__':
    main()
