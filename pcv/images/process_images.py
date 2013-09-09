import os
import sys
from collections import defaultdict

import pylab
import numpy as np
from PIL import Image

from PCV.localdescriptors import sift


def get_im(imagename):
    return Image.open(imagename).convert('L')

def get_sift_filename(imagename):
    base, ext = os.path.splitext(imagename)
    return '{}.sift'.format(base)

def plot_match(imagename1, imagename2, show=True, plot_features=True):
    '''Generate SIFT features for two images, plot their
    features onto the original images and link two-sided
    matching points with lines
    '''
    def load(filename):
        sift_filename = get_sift_filename(filename)
        if not os.path.exists(sift_filename):
            sift.process_image(filename, sift_filename)

        im = np.array(get_im(filename))
        locs, desc = sift.read_features_from_file(sift_filename)
        return im, locs, desc

    im1, locs1, desc1 = load(imagename1)
    im2, locs2, desc2 = load(imagename2)

    pylab.gray()

    # plot features on images
    if plot_features:
        sift.plot_features(im1, locs1, circle=True)
        pylab.figure()
        sift.plot_features(im2, locs2, circle=True)
        pylab.figure()

    # plot matching points
    matchscores = sift.match_twosided(desc1, desc2)
    sift.plot_matches(im1, im2, locs1, locs2, matchscores)
    pylab.figure()

    if show:
        pylab.show()


def find_similar(imagenames):
    '''Find similar images pairs
    '''
    def load(filename):
        return sift.read_features_from_file(get_sift_filename(filename))

    def score(namei, namej):
        locsi, desci = load(namei)
        locsj, descj = load(namej)

        sys.stdout.write('.')
        sys.stdout.flush()
        matches = sift.match_twosided(desci, descj)
        return sum(matches > 0)
   
    while imagenames:
        namei = imagenames.pop(0)
        if not imagenames:
            print "No match for", namei
            break

        print 'Find match for %s ' % namei,
        scores = sorted([ (score(namei, namej),
                           pos,
                           namej)
            for pos, namej in enumerate(imagenames) ],
            reverse=True)

        matchscore, pos, namej = scores[0]
        imagenames.pop(pos)

        print " ",
        if matchscore > 30:
            print "Best(%d) => %s" % (matchscore, namej)
            plot_match(namei, namej, False, False)
        else:
            print ":("

    pylab.show()



if __name__ == '__main__':
    plot_match(sys.argv[1], sys.argv[2])
    #find_similar(sys.argv[1:])
