import os
import sys

import pylab
import numpy as np
from PIL import Image

from PCV.localdescriptors import sift


def get_im(imagename):
    #return Image.open(imagename)
    return Image.open(imagename).convert('L')

def get_sift_filename(imagename):
    base, ext = os.path.splitext(imagename)
    return '{}.sift'.format(base)

def plot_sift():
    for each in sys.argv[1:]:
        sift_filename = get_sift_filename(each)
        if not os.path.exists(sift_filename):
            sift.process_image(each, sift_filename)

        locs, desc = sift.read_features_from_file(sift_filename)

        im = get_im(each)
        pylab.figure()
        sift.plot_features(im, locs, circle=True)


def plot_match():
    def load(filename):
        im = np.array(get_im(filename))
        locs, desc = sift.read_features_from_file(get_sift_filename(filename))
        return im, locs, desc

    im1, locs1, desc1 = load(sys.argv[1])
    im2, locs2, desc2 = load(sys.argv[2])

    matchscores = sift.match(desc1, desc2)
    sift.plot_matches(im1, im2, locs1, locs2, matchscores)


def main():
    pylab.gray()
    plot_sift()
    plot_match()
    pylab.show()


if __name__ == '__main__':
    main()
