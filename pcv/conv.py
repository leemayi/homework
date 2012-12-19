import sys
import math
from PIL import Image
import numpy as np
from scipy.ndimage import filters
from imtools import *
from utils import *


def kernel(sigma, order=0):
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

    if order == 1 : # first derivative
        weights[lw] = 0.0
        for ii in range(1, lw + 1):
            x = float(ii)
            tmp = -x / sd * weights[lw + ii]
            weights[lw + ii] = -tmp
            weights[lw - ii] = tmp
    elif order == 2: # second derivative
        weights[lw] *= -1.0 / sd
        for ii in range(1, lw + 1):
            x = float(ii)
            tmp = (x * x / sd - 1.0) * weights[lw + ii] / sd
            weights[lw + ii] = tmp
            weights[lw - ii] = tmp
    elif order == 3: # third derivative
        weights[lw] = 0.0
        sd2 = sd * sd
        for ii in range(1, lw + 1):
            x = float(ii)
            tmp = (3.0 - x * x / sd) * x * weights[lw + ii] / sd2
            weights[lw + ii] = -tmp
            weights[lw - ii] = tmp
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

def convolution(im, weights, axis=0):
    weights = weights[::-1]
    im2 = _make_output(im)
    for i in range(im.shape[axis]):
        if axis == 0:
            _conv_line(im[i,:], weights, im2[i,:])
        else:
            _conv_line(im[:,i], weights, im2[:,i])
    return im2

def my_gaussian_filter1d(input, sigma, axis=0, order=0):
    weights = kernel(sigma, order)
    return convolution(input, weights, axis)

def my_gaussian_filter(input, sigma, orders=(0, 0)):
    xweights = kernel(sigma, orders[0])
    yweights = kernel(sigma, orders[1])
    im = convolution(input, xweights, 0)
    return convolution(im, yweights, 1)

def my_sobel(input):
    im = convolution(input, [1,2,1], 0)
    return convolution(im, [1,0,-1], 1)


def test_my_gaussian():
    fname = '/home/huanghao/Pictures/Photos/David-Bowie-I.jpg'
    im = array(Image.open(fname).convert('L'))
    sigma = 1

    im2 = convolution(im, kernel(sigma, 1), 1)
    #im2 = filters.gaussian_filter1d(im, 1, 0, 1)
    showim(im2)

def test_my_sobel():
    fname = '/home/huanghao/Pictures/Photos/David-Bowie-I.jpg'
    im = array(Image.open(fname).convert('L'))

    im2 = my_sobel(im)
    showim(im2).convert('L').save('head.jpg')

def main():
    fname = sys.argv[1]
    im = array(Image.open(fname).convert('L'))

    imx = zeros(im.shape)
    filters.sobel(im, 1, imx)
    imy = zeros(im.shape)
    filters.sobel(im, 0, imy)
    mag = sqrt(imx**2 + imy**2)
    showim(mag)

    saveim(mag, 'test.jpg')


if __name__ == '__main__':
    main()
