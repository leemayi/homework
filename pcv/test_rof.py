import sys
from PIL import Image
from numpy import *
from numpy import random
from scipy.ndimage import filters
from pylab import *
from utils import *
import rof


def test():
    im = zeros((500, 500))
    im[100:400,100:400] = 128
    im[200:300,200:300] = 255
    im = im + 30*random.standard_normal((500, 500))

    from scipy.misc import imsave
    imsave('synth_orgin.jpg', im)
    return

    U,T = rof.denoise(im, im)
    G = filters.gaussian_filter(im, 10)

    imsave('synth_rof.jpg', U)
    imsave('synth_gaussian.jpg', G)

def test2():
    im = array(Image.open('data/empire.jpg').convert('L'))
    U,T = rof.denoise(im,im)

    showim(U)

test2()
