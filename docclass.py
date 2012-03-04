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
        return sum(self.cc.vaules())

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



def sampletrain(cl):
    cl.train('Nobody owns the water.', 'good')
    cl.train('the quick rabbit jumps fences', 'good')
    cl.train('buy pharmaceuticals now', 'bad')
    cl.train('make quick money at the online casino', 'bad')
    cl.train('the quick brown fox jumps', 'good')




if __name__ == '__main__':
    cl = Classifier(getwords)
    sampletrain(cl)
    print cl.fprob('quick', 'good')
    
    
