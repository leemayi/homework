import re
import glob
import stopwords


source = dict((fname, open(fname).read())
    for fname in glob.glob('hw3data/*'))

SEP = re.compile(r'[^a-zA-Z1-9]+')

def parse(line):
    paper_id, authors, title = line.split(':::')
    authors = authors.split('::')
    return title, authors

def split(title):
    return SEP.split(title)

def ommit(word):
    return len(word) < 2 or word in stopwords.allStopWords

def mapfn1(fname, content):
    for line in content.splitlines():
        titile, authors = parse(line)

        for word in split(title):
            word = word.lower()
            if ommit(word):
                continue

            for auth in authors:
                yield ':::'.join([auth, word]), 1

def reducefn1(key, value):
    return key, len(value)

def final1(key, count):
    author, word = key.split(':::', 1)
    print '%40s %5d %20s' % (author, count, word)

def mapfn(fname, content):
    for line in content.splitlines():
        title, authors = parse(line)
        for author in authors:
            yield author, title

def reducefn(author, titles):
    wc = {}
    for title in titles:
        for word in split(title):
            word = word.lower()
            if ommit(word):
                continue

            try:
                wc[word] += 1
            except KeyError:
                wc[word] = 1
    return author, wc

def final(author, wc):
    for word, count in wc.iteritems():
        print '%40s %5d %20s' % (author, count, word)

def test():
    groups = {}
    for k,v in source.iteritems():
        for k2,v2 in mapfn(k, v):
            try:
                groups[k2].append(v2)
            except KeyError:
                groups[k2] = [v2]

    for k,v in groups.iteritems():
        final(*reducefn(k,v))

if __name__ == '__main__':
    test()
