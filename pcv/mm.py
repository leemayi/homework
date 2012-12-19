from scipy.ndimage import measurements, morphology
from numpy import *
from utils import *


fname = 'data/houses.png'
im = array(Image.open(fname).convert('L'))
im = uint8(1*(im<128))

labels, nbr_objects = measurements.label(im)
print "number of objects:", nbr_objects

im_open = morphology.binary_opening(im, ones((9,5)), iterations=2)
labels_open, nbr_objects_open = measurements.label(im_open)
print "Number of objects:", nbr_objects_open
