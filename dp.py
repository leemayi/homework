#coding: utf8
import sys


def matrix(m, n, ini=None):
    return [ ([ini]*n) for _ in range(m) ]

def matrix_chain_order(p):
    n = len(p) - 1 # number of matrix
    m, s = matrix(n, n), matrix(n, n)

    for i in range(n):
        m[i][i] = 0
    for l in range(2, n+1): # length of matrix chain
        for i in range(n-l+1): # start matrix
            j = i+l-1 # end matrix
            m[i][j] = sys.maxint
            for k in range(i, j):
                q = m[i][k] + m[k+1][j] + p[i]*p[k+1]*p[j+1]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    return m, s

def print_optimal_parens(s, i, j):
    if i == j:
        print 'A%d' % i,
    else:
        print "(",
        print_optimal_parens(s, i, s[i][j])
        print_optimal_parens(s, s[i][j]+1, j)
        print ")",

def test_matrix_chain_order():
    p = (5, 10, 3, 12, 5, 50, 6)
    m, s = matrix_chain_order(p)
    print_optimal_parens(s, 0, 5)

#test_matrix_chain_order()

def memorize(func):
    def param_hash(args, kw):
        a = map(str, args)
        b = [ map(str, [k, kw[k]]) for k in sorted(kw.iterkeys()) ]
        return hash('|'.join(a) + '|'.join(b))
    
    mem = {}
    def wrapper(*args, **kw):
        h = param_hash(args, kw)
        if h in mem:
            return mem[h]
        r = func(*args, **kw)
        mem[h] = r
        return r

    return wrapper

def lcs1(x, y):
    '''longest common subsequence'''
    m, n = len(x), len(y)
    @memorize
    def recur_c(i, j):
        if i < 0 or j < 0:
            return 0
        if x[i] == y[j]:
            return recur_c(i-1, j-1) + 1
        c1 = recur_c(i-1, j)
        c2 = recur_c(i, j-1)
        return max(c1, c2)
    return recur_c(m-1, n-1)

def lcs(x, y):
    m, n = len(x), len(y)
    c, b = matrix(m+1, n+1), matrix(m+1, n+1, ' ')
    for i in range(m+1):
        c[i][0] = 0
    for j in range(n+1):
        c[0][j] = 0
    for i in range(1, m+1):
        for j in range(1, n+1):
            if x[i-1] == y[j-1]:
                c[i][j] = c[i-1][j-1] + 1
                b[i][j] = '`'
            elif c[i-1][j] >= c[i][j-1]:
                c[i][j] = c[i-1][j]
                b[i][j] = '^'
            else:
                c[i][j] = c[i][j-1]
                b[i][j] = '<'
    return c, b

def lcs_opt(x, y):
    m, n = len(x), len(y)
    if m < n:
        small, big = m, n
        small_str, big_str = x, y
    else:
        small, big = n, m
        small_str, big_str = y, x
        
    c = [0] * (small+1)
    for i in range(1, big+1):
        for j in range(1, small+1):
            if big_str[i-1] == small_str[j-1]:
                c[j] = c[j-1] + 1
            elif c[j] >= c[j-1]:
                pass
            else:
                c[j] = c[j-1]
    return c[n]

def print_lcs(b, x, i, j):
    if i == 0 or j == 0:
        return
    if b[i][j] == '`':
        print_lcs(b, x, i-1, j-1)
        print x[i-1],
    elif b[i][j] == '^':
        print_lcs(b, x, i-1, j)
    else:
        print_lcs(b, x, i, j-1)

def print_lcs2(c, x, i, j):
    if i == 0 or j == 0:
        return
    if c[i][j] > c[i-1][j] and c[i][j] > c[i][j-1]:
        print_lcs2(c, x, i-1, j-1)
        print x[i-1],
    elif c[i-1][j] >= c[i][j-1]:
        print_lcs2(c, x, i-1, j)
    else:
        print_lcs2(c, x, i, j-1)

def test_lcs():
    x = 'ACCGGTCGAGTGCGCGGAAGCCGGCCGAA'
    y = 'GTCGTTCGGAATGCCGTTGCTCTGTAAA'
    x = 'ABCBDAB'
    y = 'BDCABA'
    print lcs_opt(x, y)
    c, b = lcs(x, y)
    m, n = len(x), len(y)
    print c[m][n]
    print_lcs(b, x, m, n)
    print
    print_lcs2(c, x, m, n)
    print
    for r in c:
        print ' '.join(map(str, r))
    for r in b:
        print ' '.join(map(str, r))

test_lcs()
