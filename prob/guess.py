import re
import random
import nltk
from nltk import FreqDist, ConditionalFreqDist, PorterStemmer
from nltk.corpus import stopwords


DEBUG = 0

GBS = set('gb fix build git repo'.split())

STOP = set(stopwords.words('english'))
SEP = re.compile(r'[^a-zA-Z0-9]+')
def tokenize(txt):
    return SEP.split(txt)

porter = PorterStemmer()
def stem(word):
    return porter.stem(word.lower())

def get_words(txt):
    def valid(word):
        return word not in STOP and len(word) > 1 and word[0].isalpha()
    def gbs(word):
        return word not in GBS

    return filter(gbs, map(stem, filter(valid, nltk.word_tokenize(txt))))

def author_mapping(author):
    author = author.lower()
    for txt in ('qiang', 'wan', 'dawei', 'bartosh'):
        if txt in author:
            author = txt
            break
    return author

def load_data(fname):
    st = 0
    msg = []
    author = None
    data = []

    def sample():
        if msg:
            data.append((''.join(msg), author))

    for line in open(fname):
        if st == 0:
            sample()
            author = author_mapping(line.strip())
            msg = []
            st = 1
        elif st == 1 and line.startswith('[[END]]'):
            st = 0
        else:
            msg.append(line)
    sample()

    return data



class Model(object):

    def summary(self):
        print self.cls_fd

    def learn(self, A):
        print len(A)
        self.cls_fd = cls_fd = FreqDist()
        pairs = []
        for x, y in A:
            cls_fd.inc(y)
            for feature in get_words(x):
                pairs.append((y, feature))
        cfd = ConditionalFreqDist(pairs)
        self.cfd = cfd

        if DEBUG:
            print cfd
            print cfd.conditions()
            #cfd.tabulate(samples=['gbs', 'build', 'spec', 'repo', 'config'])
            cfd.tabulate()
            for author in cfd.conditions():
                print 'AUTHOR:', author
                for word, count in cfd[author].items():
                    print '%5d %20s' % (count, word)

        total = 0.
        self.vocabulary = voc = set()
        for cls in cfd.conditions():
            fd = cfd[cls]
            total += fd.N()
            voc |= set(fd.keys())

        self.cls_feature_prob = cls_feature_prob = {}
        for cls in cfd.conditions():
            fd = cfd[cls]

            cls_feature_prob[cls] = wc = {}
            for word in voc:
                if word in fd:
                    wc[word] = fd.freq(word)
                else:
                    wc[word] = 1./fd.N()

    def predict(self, msg):
        doc = get_words(msg)
        ret = []
        for cls in self.cfd.conditions():
            prob = self.class_prob(cls)
            for word in self.vocabulary:
                prob *= self.class_feature_prob(cls, word, word in doc)
            ret.append((prob, cls))

        ret.sort(key=lambda i:i[0], reverse=True)
        if DEBUG:
            print ret
        return ret[0][1]

    def class_prob(self, cls):
        return self.cls_fd.freq(cls)

    def class_feature_prob(self, cls, feature, positive):
        prob = self.cls_feature_prob[cls][feature]
        return prob if positive else (1-prob)


def main():
    data = load_data('gbs.log')
    print len(data)
    random.shuffle(data)

    n = 10
    learning_set = data[:-n]
    verify_set = data[-n:]

    model = Model()
    model.learn(learning_set)
    model.summary()

    correct = 0.
    for x, y in verify_set:
        pred = model.predict(x)
        if DEBUG:
            print x
        print pred, y
        if pred == y:
            correct += 1

    ratio = correct * 100 / n
    print 'correct ratio:%.2f%%' % ratio

def test():
    pos = ['like lot']*2000 + ['simple easy']*3000 + ['enjoying lot']*1000
    neg = ['hate waste']*800 + ['simple bore']*200 + ['enjoy lot']*400 + ['enjoy']*600
    learning_set = [(x, '+') for x in pos] + [(x, '-') for x in neg]

    model = Model()
    model.learn(learning_set)
    model.summary()
    print model.predict('like simple lot')


main()
#test()
