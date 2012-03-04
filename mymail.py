#coding: utf8
import sys
import poplib
import getpass
import cPickle
import re
import email
import base64
import quopri
import mmseg

mmseg.dict_load_defaults()
PUNC = u'，。、：；！？‘“（）'

def fetch_mail_to(fname):
    client = poplib.POP3_SSL('pop.gmail.com')
    client.user('hao2dw')
    client.pass_(getpass.getpass())

    mails = []
    cnt = len(client.list()[1])
    print 'total:', cnt

    for i in range(cnt):
        try:
            msg = client.retr(i+1)
        except:
            continue
        if i % 10 == 0:
            print 'fetching ...', i+1
        mails.append(msg)

    with open(fname, 'wb') as f:
        cPickle.dump(mails, f)

def make_data():
    fetch_mail_to(sys.argv[1])

def load(fname):
    with open(fname) as f:
        obj = cPickle.load(f)
        return [ email.message_from_string('\n'.join(m[1]))
            for m in obj ]

def escsub(sub):
    a = sub.strip().split('?')
    if len(a) == 5 and a[0] == a[-1] == '=':
        if a[2] == 'B':
            return base64.decodestring(a[3]).decode(a[1])
        elif a[2] == 'Q':
            return quopri.decodestring(a[3]).decode(a[1])
    return sub
        

def extract_mail_feature(m):
    f = {}

    # from addr
    from_ = re.findall(r'<(.*?)>', m['From'])
    if from_:
        from_ = from_[0]
    else:
        from_ = m['From']
    f['FROM:'+from_] = 1

    # subject
    sub = m['Subject'].split('\n')
    if len(sub) > 1:
        sub = '\n'.join(map(escsub, sub))
    else:
        sub = escsub(sub[0])

    is_chinese = not not re.findall('[\x80-\xff].', sub.encode('utf8'))
    if is_chinese:
        words = filter(lambda i: i not in PUNC,
            [unicode(i) for i in mmseg.Algorithm(sub)])
    else:
        words = sub.split()
    for w in words:
        f[w] = f.get(w, 0) + 1

    return f


if __name__ == '__main__':
    mails = load('data/mail.small.pickle')
    for i, m in enumerate(mails):
        f = extract_mail_feature(m)
        print f
        if i>5: break

