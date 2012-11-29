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

def guess_grid(n):
    sqrt = int(math.sqrt(n))
    if sqrt*sqrt == n:
        rows = cols = sqrt
    #TODO:
    return rows, cols

def array(images):
    n = len(images)
    assert n > 0
    rows, cols = guess_grid(n)
    mode = images[0].mode
    w, h = images[0].size # assume all images have the same size
    size = (h*cols, w*rows)
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

def load_face(fname):
    im = Image.open(fname).convert('L')
    print im.size
    return im.getdata()

def convert_faces():
    with open('yalefaces/all.txt', 'w') as f:
        for fname in glob.glob('yalefaces/subject*'):
            im = Image.open(fname).convert('L')
            bname = os.path.basename(fname)
            pixels = map(str, im.getdata())
            print >> f, '%s %s' % (bname, ' '.join(pixels))

def write_yalefaces():
    faces = [load_face('yalefaces/subject%02d.normal'%i) for i in range(1,16)]
    print len(faces[0])
    dump(faces, 'faces.txt')

def show_eigenface(fname):
    faces = [ [int(float(i)) for i in line.split()]
        for line in open(fname) ]
    for face in faces:
        im = create_image(face, (320, 243))
        im.show()

#write_yalefaces()
#show_eigenface('eigenface.txt')
#show_eigenface('meanface.txt')
convert_faces()


#TODO:
# numpy for input, output
