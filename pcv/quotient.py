import sys
from PIL import Image
from numpy import array, zeros, uint8
from scipy.ndimage import filters
from utils import gridim


fname = sys.argv[1]
print fname

im = array(Image.open(fname).convert('L'), "f")
im2 = filters.gaussian_filter(im, 5)

im3 = im / im2

gridim(map(uint8, [im, im3, im2])).show()

