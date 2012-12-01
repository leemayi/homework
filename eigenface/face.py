import os
import sys
import math
import glob
import subprocess
from struct import pack
from PIL import Image


def screen_size():
    output = subprocess.check_output("xrandr | grep \\* | cut -d' ' -f4", shell=True)
    res = output.splitlines()[-1]
    return map(int, res.split('x', 1))

def create_image(data, reverse=False):
    fmt = '%dB' % len(data)
    if reverse:
        data = [ (255-i) for i in data ]
    buf = pack(fmt, *data)
    im = Image.fromstring('L', size, buf)
    return im

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
            return (rows, cols), (weight, height)
        scale -= .05
    return

def grid(images, cols=None):
    #TODO: given cols
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
    for fname in glob.glob('yalefaces/subject*'):
        im = Image.open(fname).convert('L')
        bname = os.path.basename(fname)
        subject, condition = bname.split('.', 1)
        pixels = map(str, im.getdata())
        print '%s %s %s' % (subject, condition, ' '.join(pixels))

size = (320, 243)
#size = (28, 28)
def load_txt_face(line):
    data = [int(float(i)) for i in line.split()]
    return create_image(data, size)

def show_eigenfaces():
    meanface = load_txt_face(open('meanface.txt').readline())
    #meanface.show()

    eigenfaces = map(load_txt_face, open('eigenfaces.txt').readlines())
    grid(eigenfaces).show()

def check_result():
    faces = []
    for line in open('datain.txt'):
        sub, cond, data = line.split(' ', 2)
        #sub, data = line.split(' ', 1)
        face = load_txt_face(data)
        faces.append(face)

    M = 90
    group = []
    for line in open('all.dist.txt'):
        group.append(faces[M])
        M += 1
        similar = sorted(enumerate(map(float, line.split())), key=lambda i:i[1])[:3]
        for idx, dist in similar:
            group.append(faces[idx])
        group.append(Image.new('1', size))
    grid(group).show()

def browse_faces():
    idx = load_faces()
    subjects = sorted([g[len('subject'):] for g in idx if g.startswith('subject')])
    groups = ['subject[%s-%s]'%(subjects[0], subjects[-1])]
    groups.extend([g for g in idx if not g.startswith('subject')])

    while True:
        print 'Available groups:', ' '.join(groups)
        group = raw_input('input: ')
        if group in ('q', 'exit', 'quit'):
            print 'Bye!'
            break
        if group in idx:
            grid(idx[group]).show()


if __name__ == '__main__':
    #convert_faces()
    #browse_faces()
    #show_eigenfaces()
    check_result()
