import re
import math
import random

import nltk
from nltk import FreqDist, ConditionalFreqDist, PorterStemmer
from nltk.corpus import stopwords


DEBUG = 1

GBS = set('abnorm accept accesss accumul actual'.split())

STOP = set(stopwords.words('english'))
SEP = re.compile(r'[^a-zA-Z0-9]+')
def tokenize(txt):
    return SEP.split(txt)

porter = PorterStemmer()
def stem(word):
    return porter.stem(word.lower())

def get_words(txt):
    def valid(word):
        return len(word) > 1 and word[0].isalpha()
    def gbs(word):
        return word in GBS

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

def log(n):
    return math.log(n, 2)

class Model(object):

    def summary(self):
        if DEBUG:
            print self.cls_fd
            self.tabulate()

    def learn(self, A):
        total_y = float(len(A))
        self.cls_fd = cls_fd = FreqDist()
        self.feature_fd = feature_fd = FreqDist()
        pairs = []
        for x, y in A:
            cls_fd.inc(y)
            for feature in set(get_words(x)):
                pairs.append((y, feature))
                feature_fd.inc(feature)
        cfd = ConditionalFreqDist(pairs)

        if DEBUG:
            print cfd
            print cfd.conditions()
            #cfd.tabulate(samples=['gbs', 'build', 'spec', 'repo', 'config'])
            cfd.tabulate()
            for author in cfd.conditions():
                print 'AUTHOR:', author
                for word, count in cfd[author].items():
                    print '%5d %20s' % (count, word)

        self.voc = voc = feature_fd.keys()

        self.cls_feature_prob = cls_feature_prob = {}
        self.cls_and_feature_prob = cls_and_feature_prob = {}
        for cls, total in cls_fd.items():
            fd = cfd[cls]

            cls_feature_prob[cls] = wc = {}
            for word in voc:
                if word in fd:
                    cls_feature_prob[(cls, word)] = float(fd[word]) / total
                    cls_and_feature_prob[(cls, word)] = float(fd[word]) / total_y
                else:
                    cls_feature_prob[(cls, word)] = 1. / total
                    cls_and_feature_prob[(cls, word)] = 1. / total_y

        self.feature_prob = feature_prob = {}
        for word, count in feature_fd.items():
            feature_prob[word] = count / total_y

    def I(self, word):
        s = 0.
        word_prob = self.feature_prob[word]
        #print 'p(%s)=%f' % (word, word_prob)
        for cls in self.cls_fd.keys():
            cls_prob = self.class_prob(cls)
            prob1 = self.class_feature_prob(cls, word, 1) * cls_prob
            prob2 = self.class_feature_prob(cls, word, 0) * cls_prob
            #print 'prob1=%f prob2=%f' % (prob1, prob2)
            s += prob1 * log(prob1 / (word_prob * cls_prob))
            try:
                s += prob2 * log(prob2 / ((1-word_prob) * cls_prob))
            except ValueError:
                print '##', prob2, word_prob, cls_prob
        return s

    def predict(self, msg):
        doc = get_words(msg)
        ret = []
        for cls in self.cls_fd.keys():
            prob = self.class_prob(cls)
            for word in self.voc:
                prob *= self.class_feature_prob(cls, word, word in doc)
            ret.append((prob, cls))

        ret.sort(key=lambda i:i[0], reverse=True)
        if DEBUG:
            print ret
        return ret[0][1]

    def class_prob(self, cls):
        return self.cls_fd.freq(cls)

    def class_feature_prob(self, cls, feature, positive):
        prob = self.cls_feature_prob[(cls, feature)]
        return prob if positive else (1-prob)

    def tabulate(self):
        words = tuple(self.voc)
        fmt = ''.join(['%8s'] * len(words))
        print ' ', fmt % words
        for cls in self.cls_fd.keys():
            print cls,
            fmt = ''.join(['%8.4f']*len(words))
            print fmt % tuple(self.class_feature_prob(cls, word, 1) for word in words)

        for w, i in sorted([(word, self.I(word)) for word in words], key=lambda i:i[1], reverse=1):
            print 'I(%s,author)=%f' % (w, i)

def main():
    data = load_data('gbs.log')
    print len(data)

    k = 1
    n = 10
    ret = []
    for i in range(k):
        random.shuffle(data)

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
        ret.append(ratio)
    print 'overall:', sum(ret)/len(ret)

def test():
    raw = [
    (2000, 'I really like this course and am learning a lot', '+'),
    (800,  'I really hate this course and think it is a waste of time', '-'),
    (200,  'The course is really too simple and quite a bore', '-'),
    (3000, 'The course is simple, fun and very easy to follow', '+'),
    (1000, "I'm enjoying myself a lot and learning something too", '+'),
    (400,  'I would enjoy myself a lot if I did not have to be here', '-'),
    (600,  'I did not enjoy this course enough', '-')
    ]

    #sel = set('like lot hate wast simple bore simpl easi enjoy cours'.split())
    learning_set = []
    for n, sentence, flag in raw:
        words = set(get_words(sentence))
        #words = filter(lambda i: i in sel, words)
        sent = ' '.join(words)
        learning_set += [(sent, flag)] * n

    model = Model()
    model.learn(learning_set)
#    print model.I('cour')
    model.summary()

    print model.predict('like simple lot')


main()
#test()
