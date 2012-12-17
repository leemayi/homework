import sys
from PIL import Image
from imtools import *
from pylab import *

im = array(Image.open('300px-Unequalized_Hawkes_Bay_NZ.jpg'))
im2 = histeq2(im)

hist1,_ = histogram(im, 256)
hist2,_ = histogram(im2, 256)

plot(hist1.cumsum())
figure()
plot(hist2.cumsum())
show()

