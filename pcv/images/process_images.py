import os
import sys

import pylab
import numpy as np
from PIL import Image

from PCV.localdescriptors import sift


def get_im(imagename):
    return Image.open(imagename).convert('L')

def get_sift_filename(imagename):
    base, ext = os.path.splitext(imagename)
    return '{}.sift'.format(base)

def load(filename):
    sift_filename = get_sift_filename(filename)
    if not os.path.exists(sift_filename):
        sift.process_image(each, sift_filename)

    im = np.array(get_im(filename))
    locs, desc = sift.read_features_from_file(sift_filename)
    return im, locs, desc

def plot_match(imagename1, imagename2):
    '''Generate SIFT features for two images, plot their
    features onto the original images and link two-sided
    matching points with lines
    '''
    im1, locs1, desc1 = load(imagename1)
    im2, locs2, desc2 = load(imagename2)

    pylab.gray()

    # plot features on images
    sift.plot_features(im1, locs1, circle=True)
    pylab.figure()
    sift.plot_features(im2, locs2, circle=True)
    pylab.figure()

    # plot matching points
    matchscores = sift.match_twosided(desc1, desc2)
    sift.plot_matches(im1, im2, locs1, locs2, matchscores)

    pylab.show()


def main():
    plot_match(*sys.argv[1:3])


if __name__ == '__main__':
    main()
