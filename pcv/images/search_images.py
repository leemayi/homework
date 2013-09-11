import sys
import cPickle

from PCV.localdescriptors import sift
from PCV.imagesearch.vocabulary import Vocabulary
from PCV.imagesearch.imagesearch import Indexer, Searcher

from process_images import process_image, get_sift_filename

VOC_NAME = 'douban'
VOC_FILE = 'vocabulary.%s.pkl' % VOC_NAME
DB_FILE = '%s.db' % VOC_NAME

def make_voc(imlist):
    featlist = [ process_image(im) for im in imlist ]

    voc = Vocabulary(VOC_NAME)
    voc.train(featlist, 1000, 10)

    # saving vocabulary
    with open(VOC_FILE, 'wb') as f:
        cPickle.dump(voc, f)
    print 'vocabulary', voc.name, 'has', voc.nbr_words, 'words'


def index_images(imlist):
    featlist = [ get_sift_filename(i) for i in imlist ]

    # load vocabulary
    with open(VOC_FILE, 'rb') as f:
        voc = cPickle.load(f)

    # create indexer
    indx = Indexer(DB_FILE, voc)
    indx.create_tables()

    # go through all images, project features on vocabulary and insert
    for imagefile, siftfile in zip(imlist, featlist):
        locs, descr = sift.read_features_from_file(siftfile)
        indx.add_to_index(imagefile, descr)

    indx.db_commit()

def search_image(imagename):
    with open(VOC_FILE, 'rb') as f:
        voc = cPickle.load(f)

    locs, descr = sift.read_features_from_file(get_sift_filename(imagename))
    iw = voc.project(descr)

    src = Searcher(DB_FILE, voc)
    print 'ask using a histogram ...'
    print src.candidates_from_histogram(iw)[:5]

    print 'try a query ...'
    for dist, imid in src.query(imagename)[:5]:
        cur = src.con.execute('select filename from imlist where rowid=%d' % imid)
        print '%s(%d)' % (cur.fetchone()[0], dist)


if __name__ == '__main__':
    make_voc(sys.argv[1:])
    #index_images(sys.argv[1:])
    #search_image(sys.argv[1])
