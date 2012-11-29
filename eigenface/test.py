import os
import math
import glob
from struct import unpack, pack
from PIL import Image


def read_labels(fname):
    with open(fname) as f:
        magic, total = unpack('>2I', f.read(4*2))
        assert magic == 2049
        return unpack('%dB' % total, f.read(total))

def read_images(fname):
    with open(fname) as f:
        magic, total, rows, cols = unpack('>4I', f.read(4*4))
        assert magic == 2051
        pixels = rows * cols
        fmt = '%dB' % pixels
        return (rows, cols), [ unpack(fmt, f.read(pixels))
            for _ in xrange(total) ]

def create_image(data, size, reverse=False):
    fmt = '%dB' % len(data)
    if reverse:
        data = [ (255-i) for i in data ]
    buf = pack(fmt, *data)
    im = Image.fromstring('L', size, buf)
    return im

def array(images, rows, cols):
    n = len(images)
    print n
    assert n > 0
    mode = images[0].mode
    w, h = images[0].size # assume all images have the same size
    size = (w*cols, h*rows)
    im = Image.new(mode, size)
    for r in range(rows):
        for c in range(cols):
            i = r*cols+c
            if i >= n:
                break
            im.paste(images[i], (w*c, h*r))
    return im

def dump(data, fname):
    with open(fname, 'w') as f:
        for im in data:
            line = ' '.join([ str(p) for p in im ])
            f.write(line+'\n')

def write_numbers():
    n = 16
    labels = read_labels('MNIST/t10k-labels-idx1-ubyte')[:n]
    size, data = read_images('MNIST/t10k-images-idx3-ubyte')
    data = data[:n]
    dump(data, 'numbers.txt')

def load_faces():
    index = {}
    for fname in sorted(glob.glob('yalefaces/subject*')):
        bname = os.path.basename(fname) 
        subject, condition = bname.split('.', 1)
        im = Image.open(fname).convert('L')
        index.setdefault(subject, []).append(im)
        index.setdefault(condition, []).append(im)
        index.setdefault('all', []).append(im)
    return index

def convert_faces():
    with open('yalefaces/all.txt', 'w') as f:
        for fname in glob.glob('yalefaces/subject*'):
            im = Image.open(fname).convert('L')
            bname = os.path.basename(fname)
            pixels = map(str, im.getdata())
            print >> f, '%s %s' % (bname, ' '.join(pixels))

def load_txt_face(line):
    data = [int(float(i)) for i in line.split()]
    return create_image(data, (320, 243))

def show_eigenface():
    faces = [ load_txt_face(line).resize((320/4, 243/4))
        for line in open('eigenfaces.txt') ]
    array(faces, 10, 13).show()

show_eigenface()
#write_yalefaces()
#show_eigenface('eigenface.txt')
#show_eigenface('meanface.txt')
#convert_faces()

#faces = load_faces()
#array(faces['normal'], 4, 4).show()
#array(faces['subject07'], 3, 4).show()

#TODO:
# numpy for input, output
