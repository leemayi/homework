from PIL import Image
from numpy import *
from scipy.ndimage import filters
from imtools import *


if 0:
    im = array(Image.open('data/empire.jpg').convert('L'))
    im2 = filters.gaussian_filter(im, 5)
    showim(im2)
else:
    im = array(Image.open('data/empire.jpg'))
    im2 = zeros(im.shape)
    for i in range(3):
        im2[:,:,i] = filters.gaussian_filter(im[:,:,i], 5)
    im2 = uint8(im2)
    showim(im2)
