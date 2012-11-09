import sys
import cPickle
import os

from cluster import read_file, tanimoto


def trans_data():
    codes = set()
    users = {}

    for line in sys.stdin:
        phone, servcode = line.rstrip().split('|')
        servcode = servcode.strip()
        if not servcode:
            continue

        try:
            users[phone].add(servcode)
        except KeyError:
            users[phone] = set([servcode])
        codes.add(servcode)

    code_cnt = len(codes)
    cid2name = dict(enumerate(codes))

    # title
    print '\t'.join(['user'] + [cid2name[cid] for cid in range(code_cnt)])

    uid = 0
    for _, services in users.iteritems():
        row = [str(uid)] + \
            [('1' if cid2name[cid] in services else '0')
                for cid in range(code_cnt)]
        uid += 1
        print '\t'.join(row)

def transpose(data):
    r, c = len(data), len(data[0])
    data2 = [None]*c
    for i in range(c):
        data2[i] = [None]*r
        for j in range(r):
            data2[i][j] = data[j][i]
    return data2

def sim_tanimoto(*args):
    return 1.0 - tanimoto(*args)

def similarity_matrix(vectors, similarity=sim_tanimoto):
    n = len(vectors)
    m = [None]*n

    for i in range(n):
        m[i] = [None]*n
        for j in range(i+1, n):
            m[i][j] = similarity(vectors[i], vectors[j])
    for i in range(n):
        for j in range(0, i+1):
            if i == j:
                m[i][j] = 2 # self
            else:
                m[i][j] = m[j][i]
    return m

def recommendation(cube, items, n=5):
    res = {}
    for rid, row in enumerate(cube):
        idx_row = [i for i in enumerate(row)]
        idx_row.sort(lambda i,j: -1*cmp(i[1], j[1]))
        top = [ (cid,sim) for cid,sim in idx_row[1:n+1] if sim>0 ] # the first is self
        if top:
            res[items[rid]] = [ (sim, items[cid]) for cid,sim in top ]
    return res

def main():
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        f = sys.argv[1]
    else:
        f = sys.stdin
    userids, services, data = read_file(f)
    items = transpose(data)
    m = similarity_matrix(items)
    '''
    for row in m:
        for col in row:
            if col is None:
                print '_',
            else:
                print '%.2g'%col,
        print
    '''

    result = recommendation(m, services)
    print 'res:', len(result)
    for item, rec in result.iteritems():
        print '-'*10, item
        for sim, item2 in rec:
            print '%4.2g %5s' % (sim, item2),
        print


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'trans':
        trans_data()
    else:
        main()
