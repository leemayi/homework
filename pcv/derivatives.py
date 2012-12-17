from PIL import Image
from numpy import *
from scipy.ndimage import filters
from imtools import *
from utils import grid, toimg


def trans(im, func):
    imx = zeros(im.shape)
    func(im, 1, imx)

    imy = zeros(im.shape)
    func(im, 0, imy)

    magnitude = sqrt(imx**2 + imy**2)
    return imx, imy, magnitude

def sobel(im, axis, im2):
    filters.sobel(im, axis, im2)

def prewitt(im, axis, im2):
    filters.prewitt(im, axis, im2)

def gaussian(im, axis, im2):
    sigma = 3
    filters.gaussian_filter(im, (sigma, sigma), (1-axis, axis), im2)

def main():
    fname = 'data/empire.jpg'
    img = Image.open(fname).convert('L')
    #img.thumbnail((500, 500))

    im = array(img)
    pics = [img]
    for func in (sobel, gaussian, prewitt):
        pics.extend(map(toimg, trans(im, func)))
    grid(pics).show()

main()
