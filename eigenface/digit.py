from struct import unpack
from PIL import Image
from face import grid, create_image


def read_labels(fname):
    with open(fname) as f:
        magic, total = unpack('>2I', f.read(4*2))
        assert magic == 2049
        return unpack('%dB' % total, f.read(total))

size = None
def read_images(fname):
    with open(fname) as f:
        magic, total, rows, cols = unpack('>4I', f.read(4*4))
        assert magic == 2051
        global size
        size = (rows, cols)
        pixels = rows * cols
        fmt = '%dB' % pixels
        return [ unpack(fmt, f.read(pixels))
                 for _ in xrange(total) ]

def dump(data, fname):
    with open(fname, 'w') as f:
        for im in data:
            line = ' '.join([ str(p) for p in im ])
            f.write(line+'\n')

def convert_to_txt():
    n = 200
    labels = read_labels('MNIST/t10k-labels-idx1-ubyte')[:n]
    digits = read_images('MNIST/t10k-images-idx3-ubyte')[:n]

    images = [create_image(i) for i in digits]
    grid(images).show()

    for i in range(n):
        print labels[i], ' '.join(map(str, digits[i]))


if __name__ == '__main__':
    convert_to_txt()
