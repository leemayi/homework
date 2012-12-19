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

def my_gaussian_filter(input, sigma, order=0):
    weights = kernel(sigma, order)
    im = convolution(input, weights, 0)
    return convolution(im, weights, 1)

def my_sobel(input):
    im = convolution(input, [1,2,1], 0)
    return convolution(im, [1,0,-1], 1)


def main():
    fname = 'data/empire.jpg'
    fname = '/home/huanghao/Downloads/title.png'
    img = Image.open(fname).convert('L')
    im = array(img)

    sigma = 1
    im2 = my_gaussian_filter(im, sigma, 0)
    showim(im2)
    #im3 = filters.gaussian_filter(im, sigma)

    #grid([img, toimg(im2), toimg(im3)]).show()

def test():
    fname = '/home/huanghao/Pictures/Photos/David-Bowie-I.jpg'
    im = array(Image.open(fname).convert('L'))

    im2 = my_sobel(im)
    showim(im2).convert('L').save('head.jpg')



if __name__ == '__main__':
    main()
