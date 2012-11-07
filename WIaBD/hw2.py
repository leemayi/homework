import re
import math


def log(n):
    if n == 0:
        n = 1
    return math.log(n, 2)


positive, negative = 1, 0



def stem(word):
    if word.endswith('ing'):
        return word[:-3]
    if word.endswith('ed'):
        return word[:-2]
    return word


def split(sentence):
    return [ stem(w) for w in re.split(r'[^a-zA-Z]+', sentence.lower()) ]


def learning(data):
    total = [0., 0.]
    wf = {}
    for cnt, comment, sentiment in data:
        total[sentiment] += cnt
        for word in split(comment):
            try:
                wf[word][sentiment] += cnt
            except KeyError:
                # neg cnt, pos cnt, neg pro, pos pro, mutual infor
                if sentiment:
                    wf[word] = [0., float(cnt), None, None, None]
                else:
                    wf[word] = [float(cnt), 0., None, None, None]

    cnt = total[positive] + total[negative]
    p_positive = total[positive] / cnt
    p_negative = 1 - p_positive

    print '%40s%40s' % (
        'p(+) = %d/%d = %.2g;' % (total[positive], cnt, p_positive),
        'p(-) = %d/%d = %.2g;' % (total[negative], cnt, p_negative)
        )
        
    for word, val in wf.iteritems():
        cnt_n, cnt_p = val[:2]
        if cnt_p == 0:
            cnt_p = 1
        if cnt_n == 0:
            cnt_n = 1

        pn = cnt_n/total[negative]
        pp = cnt_p/total[positive]
        val[2], val[3] = pn, pp
        # Sigma { p(f,b) * log(p(f,b) / (p(f)*p(b))) }
        '''
        val[4] = \
            (cnt_p/cnt) * log((cnt_p/cnt) / (p_positive * ((cnt_n+cnt_p)/cnt))) + \
            ((total[positive]-cnt_p)/cnt) * log(((total[positive]-cnt_p)/cnt) / (p_positive * (1-(cnt_n+cnt_p)/cnt))) + \
            (cnt_n/cnt) * log((cnt_n/cnt) / (p_negative * ((cnt_n+cnt_p)/cnt))) + \
            ((total[negative]-cnt_n)/cnt) * log(((total[negative]-cnt_n)/cnt) / (p_negative * (1-(cnt_n+cnt_p)/cnt)))
        '''

        print '%40s%40s%30s' % (
            'p(%s|+) = %d/%d = %.2g;' % (word, cnt_p, total[positive], pp),
            'p(%s|-) = %d/%d = %.2g;' % (word, cnt_n, total[negative], pn),
            #'I(%s,S) = %.2g;' % (word, val[4]),
            '',
            )

    return wf, p_positive, p_negative


def predict(comment, wf, p_positive, p_negative, selected):
    numerator = 1.
    denominator = 1.
    words = set(split(comment))
    for word in selected:
        if word in words:
            numerator *= wf[word][3]
            denominator *= wf[word][2]
        else:
            numerator *= 1-wf[word][3]
            denominator *= 1-wf[word][2]
    numerator *= p_positive
    denominator *= p_negative
    L = numerator / denominator

    print comment
    print 'L = %.2g/%.2g = %.2g' % (numerator, denominator, L)
    return L


def select(wf, selected):
    nwf = {}
    for word in selected:
        try:
            nwf[word] = wf[word]
        except KeyError:
            pass
    return nwf



def test1():
    data = [
    (2000, "I really like this course and am learning a lot", positive),
    (800, "I really hate this course and think it is a waste of time", negative),
    (200, "The course is really too simple and quite a bore", negative),
    (3000, "The course is simple, fun and very easy to follow", positive),
    (1000, "I'm enjoying this course a lot and learning something too", positive),
    (400, "I would enjoy myself a lot if I did not have to be in this course", negative),
    (600, "I did not enjoy this course enough", negative),
    ]

    selected = ("like", "lot", "hate", "waste", "simple", "easy", "enjoy")

    wf, p_positive, p_negative = learning(data)
    new = "I really like this simple course a lot"
    predict(new, select(wf, selected), p_positive, p_negative, selected)


def test2():
    data = [
    #   instances Tweet /   Comment Sentiment
    (2000, "My phone   is  really  bad and gives   me  lots    of  trouble", negative),
    (5000, "I  really  like my phone   because it  helps   me  enjoy life", positive),
    (5000, "My new phone   is  a   pleasure to use and very    nice", positive),
    (3000, "I  hate this   phone,  it  is  making  my  life    miserable", negative),
    ]

    selected = ("bad", "trouble", "like", "enjoy", "pleasure", "nice", "hate", "miserable")

    wf, p_positive, p_negative = learning(data)
    nwf = select(wf, selected)

    for _, sentence, _ in data:
        predict(sentence, nwf, p_positive, p_negative, selected)
        print

    for sentence in (
        "the new Y777 appears nice but is a lot of trouble",
        "the new Y777 is really nice even though it gives trouble sometimes",
        "the K677 is a really bad phone and I hate it",
        "I really like my new K677, it is a pleasure to use",
        ):
        predict(sentence, nwf, p_positive, p_negative, selected)
        print


test2()
