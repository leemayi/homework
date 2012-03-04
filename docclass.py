import re
import math

def getwords(doc):
    splitter = re.compile('\\W*')
    words = [ s.lower() for s in splitter.split(doc)
        if len(s) > 2 and len(s) < 20 ]
    return dict([(w, 1) for w in words])

class Classifier(object):

    def __init__(self, getfeatures, filename=None):
        self.fc = {}
        self.cc = {}
        self.getfeatures = getfeatures
        self.thresholds = {}

    def incf(self, f, cat):
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1

    def incc(self, cat):
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1

    def fcount(self, f, cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.

    def catcount(self, cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0

    def totalcount(self):
        return sum(self.cc.values())

    def categories(self):
        return self.cc.keys()

    def train(self, item, cat):
        features = self.getfeatures(item)
        for f in features:
            self.incf(f, cat)
        self.incc(cat)

    def fprob(self, f, cat):
        if self.catcount(cat) == 0:
            return 0
        return self.fcount(f, cat) / self.catcount(cat)

    def weightedprob(self, f, cat, prf, weight=1., ap=.5):
        basicprob = prf(f, cat)
        totals = sum([self.fcount(f,c) for c in self.categories()])
        bp = (weight*ap + totals*basicprob) / (weight+totals)
        return bp

    def set_threshold(self, cat, t):
        self.thresholds[cat] = t

    def get_threshold(self, cat):
        return self.thresholds.get(cat, 1.)

    def classify(self, item, default=None):
        probs = {}
        max_ = 0.
        best = default

        for cat in self.categories():
            probs[cat] = self.prob(item, cat)
            if probs[cat] > max_:
                max_ = probs[cat]
                best = cat

        for cat in probs:
            if cat == best:
                continue
            if probs[cat] * self.get_threshold(best) > probs[best]:
                return default
        return best


def sampletrain(cl):
    cl.train('Nobody owns the water.', 'good')
    cl.train('the quick rabbit jumps fences', 'good')
    cl.train('buy pharmaceuticals now', 'bad')
    cl.train('make quick money at the online casino', 'bad')
    cl.train('the quick brown fox jumps', 'good')

class NaiveBayes(Classifier):

    def docprob(self, item, cat):
        features = self.getfeatures(item)
        p = 1
        for f in features:
            p *= self.weightedprob(f, cat, self.fprob)
        return p

    def prob(self, item, cat):
        catprob = self.catcount(cat) / self.totalcount()
        docprob = self.docprob(item, cat)
        return docprob * catprob

class FisherClassifier(Classifier):

    def __init__(self, getfeatures):
        super(FisherClassifier, self).__init__(getfeatures)
        self.minimums = {}

    def cprob(self, f, cat):
        clf = self.fprob(f, cat)
        if clf == 0:
            return 0
        freqsum = sum([self.fprob(f, c) for c in self.categories()])
        p = clf/ freqsum
        return p

    def fisherprob(self, item, cat):
        p = 1
        features = self.getfeatures(item)
        for f in features:
            p *= self.weightedprob(f, cat, self.cprob)
        fscore = -2 * math.log(p)
        return self.invchi2(fscore, len(features)*2)

    def invchi2(self, chi, df):
        m = chi / 2.
        sum_ = term = math.exp(-m)
        for i in range(1, df/2):
            term *= m / i
            sum_ += term
        return min(sum_, 1.)

    def set_minimum(self, cat, min_):
        self.minimums[cat] = min

    def get_minimum(self, cat):
        return self.minimums.get(cat, 0)

    def classify(self, item, default=None):
        best = default
        max_ = 0.
        for c in self.categories():
            p = self.fisherprob(item, c)
            if p > self.get_minimum(c) and p > max_:
                best = c
                max_ = p
        return best



def bayes():
    cl = NaiveBayes(getwords)
    sampletrain(cl)
    print cl.classify('quick rabbit', default='unknown')
    print cl.classify('quick money', default='unknown')
    cl.set_threshold('bad', 3)
    print cl.classify('quick money', default='unknown')
    for i in range(10):
        sampletrain(cl)
    print cl.classify('quick money', default='unknown')

def fisher():
    cl = FisherClassifier(getwords)
    sampletrain(cl)
    print cl.classify('quick rabbit')
    print cl.classify('quick money')
    cl.set_minimum('bad', .8)
    print cl.classify('quick money')
    cl.set_minimum('good', .4)
    print cl.classify('quick money')


if __name__ == '__main__':
    fisher()
