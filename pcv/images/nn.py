from numpy import zeros
from pyflann import FLANN


def match(desc1, desc2, dist_ratio=0.6, num_trees=4):
    flann = FLANN()
#    result, dists = flann.nn(desc2, desc1, 2, algorithm="kmeans",
#                             branching=32, iterations=7, checks=16)
    result, dists = flann.nn(desc2, desc1, 2,
                             algorithm='kdtree', trees=num_trees)

    matchscores = zeros((desc1.shape[0]), 'int')
    for idx1, (idx2, _idx_second_nearest) in enumerate(result):
        nearest, second_nearest = dists[idx1]
        if nearest < dist_ratio * second_nearest:
            matchscores[idx1] = idx2
    return matchscores


def match_twosided(desc1,desc2):
    """ Two-sided symmetric version of match(). """
    
    matches_12 = match(desc1,desc2)
    matches_21 = match(desc2,desc1)
    
    ndx_12 = matches_12.nonzero()[0]
    
    # remove matches that are not symmetric
    for n in ndx_12:
        if matches_21[int(matches_12[n])] != n:
            matches_12[n] = 0
    
    return matches_12
