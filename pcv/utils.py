import sys
import math
import subprocess
from PIL import Image
import scipy

def screen_size():
    output = subprocess.check_output("xrandr | grep \\* | cut -d' ' -f4", shell=True)
    res = output.splitlines()[-1]
    return map(int, res.split('x', 1))

def guess_grid(screen_size, image_size, n):
    screen_weight, screen_height = screen_size
    image_weight, image_height = image_size
    scale = 1
    while True:
        if scale <= 0:
            break
        weight, height = int(image_weight*scale), int(image_height*scale)
        cols = screen_weight / weight
        rows = screen_height / height
        if cols * rows >= n:
            rows = int(math.ceil(float(n)/cols))
            if rows == 1:
                cols = min(n, cols)
            return (rows, cols), (weight, height)
        scale -= .02

def grid(images, cols=None, padding=None):
    #TODO: given cols, padding
    n = len(images)
    assert n > 0

    ss = map(lambda i:int(i*.9), screen_size())
    (rows, cols), (w, h) = guess_grid(ss, images[0].size, n)
    print >> sys.stderr, 'show %d images by (%d, %d)' % (n, rows, cols)
    size = (w*cols, h*rows)

    im = Image.new(images[0].mode, size)
    for r in range(rows):
        for c in range(cols):
            i = r*cols+c
            if i >= n:
                break
            im.paste(images[i].resize((w, h)), (w*c, h*r))
    return im

def gridim(ims):
    return grid(map(toimg, ims))

def showim(im):
    img = Image.fromarray(im)
    img.show()
    return img

def toimg(im):
    return Image.fromarray(im)

def saveim(im, fname):
    return scipy.misc.imsave(fname, im)

def histeq2(im):
    dim = im.shape
    hist = [0]*256
    im = im.flatten()
    for level in im:
        hist[level] += 1

    cdf = hist
    for i in range(1, len(hist)):
        cdf[i] += cdf[i-1]

    cdf_min = None
    h = cdf
    for v, cdfv in enumerate(cdf):
        if cdfv == 0:
            continue
        if cdf_min is None:
            cdf_min = cdfv
        h[v] = round(255. * (cdfv - cdf_min) / (cdf[-1] - cdf_min))

    for i, v in enumerate(im):
        im[i] = h[v]
    return im.reshape(dim)
