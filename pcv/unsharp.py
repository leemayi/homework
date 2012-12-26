import sys
from PIL import Image
from numpy import array, zeros, uint8
from scipy.ndimage import filters
from utils import gridim


fname = sys.argv[1]
print fname

im = array(Image.open(fname), dtype='f')
im2 = zeros(im.shape)
for i in range(3):
    im2[:,:,i] = filters.gaussian_filter(im[:,:,i], 3)
im2 = im2

im3 = im - .15*im2

gridim(map(uint8, [im, im3, im2])).show()

