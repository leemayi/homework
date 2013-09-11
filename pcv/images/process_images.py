import os
import sys
from collections import defaultdict

import pylab
import numpy as np
from PIL import Image
from PCV.localdescriptors import sift

import nn


class MyImage(object):

    def __init__(self, filename):
        self.filename = filename
        self.im, self.locs, self.desc = load(self.filename)

def get_im(imagename):
    return Image.open(imagename)

def get_sift_filename(imagename):
    base, ext = os.path.splitext(imagename)
    return '{}.sift'.format(base)

def process_image(filename):
    sift_filename = get_sift_filename(filename)
    if not os.path.exists(sift_filename):
        sift.process_image(filename, sift_filename)
    return sift_filename

def load(filename):
    sift_filename = process_image(filename)
    im = np.array(get_im(filename))
    locs, desc = sift.read_features_from_file(sift_filename)
    return im, locs, desc


def plot_match(imagename1, imagename2, show=True, plot_features=True):
    '''Generate SIFT features for two images, plot their
    features onto the original images and link two-sided
    matching points with lines
    '''
    pylab.gray()

    # plot features on images
    # plot matching points
    # matchscores = sift.match_twosided(desc1, desc2)
    matchscores = nn.match_twosided(desc1, desc2)
    sift.plot_matches(im1, im2, locs1, locs2, matchscores)
    pylab.figure()

    if show:
        pylab.show()


def find_similar(imagenames, plot_features=False):
    '''Find similar images pairs
    '''
    first_figure = True
    images = [ MyImage(i) for i in imagenames ]
    matches = defaultdict(list)
    length = len(images)

    if plot_features:
        for image in images:
            if first_figure:
                first_figure = False
            else:
                pylab.figure()
            sift.plot_features(image.im, image.locs, circle=True)

    for i in range(length):
        this = images[i]
        print 'Find match for', this.filename, ' ',
        for j in range(i+1, length):
            that = images[j]
            sys.stdout.write('.')
            sys.stdout.flush()
            
            matched_points = nn.match_twosided(this.desc, that.desc)
            similarity = sum(matched_points > 0)

            matches[i].append((similarity, j, matched_points))
            matches[j].append((similarity, i, matched_points))
        print ' ',

        # at least 10 points matched
        # and only need top 3 matches
        scores = sorted([k for k in matches[i]
                         if k[0] > 10 ], reverse=True)[:3]
        if not scores:
            print 'No match :('
        else:
            for sim, k, matched_points in scores:
                that = images[k]
                print '%s(%d) ' % (that.filename, sim),

                if first_figure:
                    first_figure = False
                else:
                    pylab.figure()

                if k < i: # only cal the top right triangle
                    this = images[k]
                    that = images[i]
                sift.plot_matches(this.im, that.im,
                                  this.locs, that.locs,
                                  matched_points)
            print

    pylab.show()



if __name__ == '__main__':
    find_similar(sys.argv[1:])
