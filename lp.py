import sys
import pulp
import sympy
import re


var = re.compile(r'[_a-zA-Z][_a-zA-Z0-9]*')
logic_ops = ('>=', '<=', '==', '>', '<')
debug = 0

def extract_var(ex):
    return set(re.findall(var, ex))

def solve(definition):
    print >> sys.stderr, '-'*20, 'problem'
    print >> sys.stderr, definition

    if debug > 1: print >> sys.stderr, '-'*20, 'parse'
    exs, vars_, target, cat, mm = parse(definition)

    if debug > 1: print >> sys.stderr, '-'*20, 'setup'
    prob, target2, lpvar = setup(exs, vars_, target, cat, mm)

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
    print 'target:', eval(target, res), '=', target2

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
            vars_ |= extract_var(target)
        elif line[:3].lower() == 'cat':
            cat = line.split(None, 1)[1]
        else:
            st, var = parse_st(line)
            exs.extend(st)
            vars_ |= var
    return exs, vars_, target, cat, mm

def parse_st(line):
    '''st formatting as follow:
    x1 > 1
    2 > x2
    x3,x4>=0
    '''
    for op in logic_ops:
        if op in line:
            left, right = line.split(op, 1)
            break

    if ',' in left:
        sub = left.split(',')
    else:
        sub = [left]

    st = []
    var = set()
    for left in sub:
        var |= extract_var(left)
        st.append('%s %s %s' % (left, op, right))
    return st, var

def setup(exs, vars_, target, cat, mm):
    sym, lpvar = {}, {}
    for n in vars_:
        sym[n] = sympy.Symbol(n)
        lpvar[n] = pulp.LpVariable(n, cat=cat)

    target = eval(target, sym)
    st = [str(target)]
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
    return prob, target, lpvar



