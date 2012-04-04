import sys
import pulp
import sympy
import re


delimiter = re.compile(r'[+\-=*/><() \t\n]')
var = re.compile(r'[_a-zA-Z][_a-zA-Z0-9]*')
logic_ops = ('>=', '<=', '==', '>', '<')
debug = 0

def extract_var(ex):
    return filter(var.match, re.split(delimiter, ex))

def solve(definition):
    print >> sys.stderr, '-'*20, 'problem'
    print >> sys.stderr, definition

    if debug > 1: print >> sys.stderr, '-'*20, 'parse'
    exs, vars_, target, cat, mm = parse(definition)

    if debug > 1: print >> sys.stderr, '-'*20, 'setup'
    prob, lpvar = setup(exs, vars_, target, cat, mm)

    if debug > 1: print >> sys.stderr, '-'*20, 'solve'
    status = prob.solve(pulp.GLPK(msg=0))

    print >> sys.stderr, '-'*20, 'result'
    print pulp.LpStatus[status]

    def sort_var_name(x, y):
        t = cmp(len(x), len(y))
        return t if t != 0 else cmp(x, y)

    res = {}
    for n in sorted(vars_, sort_var_name):
        v = pulp.value(lpvar[n])
        res[n] = v
        print n, ':', v
    print 'target:', eval(target, res)

def parse(definition):
    exs = []
    vars_ = set()
    target = None
    cat = 'Continuous'

    for line in definition.split('\n'):
        line = line.strip()

        if not line or line.startswith('#'):
            continue
        elif line[:3].lower() in ('min', 'max'): #TODO:
            mm, target = line.split(None, 1)
            mm = mm.lower() # min or max
            vars_ |= set(extract_var(target))
        elif line[:3].lower() == 'cat':
            cat = line.split(None, 1)[1]
        else:
            exs.append(line)
            vars_ |= set(extract_var(line))
    return exs, vars_, target, cat, mm

def setup(exs, vars_, target, cat, mm):
    sym, lpvar = {}, {}
    for n in vars_:
        sym[n] = sympy.Symbol(n)
        lpvar[n] = pulp.LpVariable(n, cat=cat)

    st = [str(eval(target, sym))]
    for ex in exs:
        for op in logic_ops:
            if op in ex:
                left, right = ex.split(op, 1)
                ex2 = '%s-(%s)'%(left, right)
                ex3 = '%s %s 0' % (str(eval(ex2, sym)), op)
                st.append(ex3)
                break

    mm = pulp.LpMinimize if mm == 'min' else pulp.LpMaximize
    prob = pulp.LpProblem('__anonymous__', mm)
    for ex in st:
        tmp = eval(ex, lpvar)
        if debug > 1: print 's.t.', tmp
        prob += tmp
    return prob, lpvar


def test1():
    solve('''
min x
#cat Integer

x - 100 - w1 - w2 == y1
1.04*y1 - 150 - w3 == y2
1.04*y2 - 120 + 1.25*w2 == y3
1.04*y3 + 1.4*w1 + 1.3*w3 == 110
x >= 0
y1 >= 0
y2 >= 0
y3 >= 0
w1 >= 0
w2 >= 0
w3 >= 0
w1 <= 60
w2 <= 90
w3 <= 50
''')


def test2():
    solve('''
max 2*x1 + x2

5*x2 <= 15
6*x1 + 2*x2 <= 24
x1 + x2 <= 5
x1 >= 0
x2 >= 0
''')

def test3():
    solve('''
max 2*x1 + 3*x2 + x3

x1 + x3 == 5
x1 + 2*x2 + x4 == 10
x2 + x5 == 4
x1 >= 0
x2 >= 0
x3 >= 0
x4 >= 0
x5 >= 0
''')


debug = 1
test1()
