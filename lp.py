import sys
import pulp
import sympy
import re


class Prob(object):

    delimiter = re.compile(r'[+\-=*/><() \t\n]')
    var = re.compile(r'[_a-zA-Z][_a-zA-Z0-9]*')
    logic_ops = ('>=', '<=', '==', '>', '<')

    def __init__(self, name, definition):
        print >> sys.stderr, '-'*20, 'problem'
        print >> sys.stderr, definition

        exs = []
        vars_ = set()
        target = None
        cat = 'Continuous'

        print >> sys.stderr, '-'*20, 'parse'
        for line in definition.split('\n'):
            line = line.strip()

            if not line or line.startswith('#'):
                continue
            elif line[:3].lower() in ('min', 'max'): #TODO:
                mm, target = line.split(None, 1)
                mm = mm.lower() # min or max
                vars_ |= set(self.parse_var(target))
            elif line[:3].lower() == 'cat':
                cat = line.split(None, 1)[1]
            else:
                exs.append(line)
                vars_ |= set(self.parse_var(line))

        sym, lpvar = {}, {}
        for n in vars_:
            sym[n] = sympy.Symbol(n)
            lpvar[n] = pulp.LpVariable(n, cat=cat)

        st = [str(eval(target, sym))]
        for ex in exs:
            for op in self.logic_ops:
                if op in ex:
                    left, right = ex.split(op, 1)
                    ex2 = '%s-(%s)'%(left, right)
                    ex3 = '%s %s 0' % (str(eval(ex2, sym)), op)
                    st.append(ex3)
                    break

        print >> sys.stderr, '-'*20, 'setup'
        mm = pulp.LpMinimize if mm == 'min' else pulp.LpMaximize
        prob = pulp.LpProblem(name, mm)
        for ex in st:
            tmp = eval(ex, lpvar)
            prob += tmp

        print >> sys.stderr, '-'*20, 'result'
        status = prob.solve(pulp.GLPK(msg=0))
        print pulp.LpStatus[status]

        res = {}
        for n in sorted(vars_):
            v = pulp.value(lpvar[n])
            res[n] = v
            print n, ':', v
        print 'target:', eval(target, res)


    @classmethod
    def parse_var(cls, ex):
        return filter(cls.var.match, re.split(cls.delimiter, ex))



def test1():
    prob = '''
min x1
#cat Integer

x1 >= 100
x2 >= 150
x3 >= 120
x4 >= 110
(x1 - 100 - 60*y1 - 90*y2) * 1.04 == x2
(x2 - 150 - 50*y3 + 112.5*y2) * 1.04 == x3
(x3 - 120 + 84*y1 + 65*y3) * 1.04 == x4
y1 >= 0
y2 >= 0
y3 >= 0
y1 <= 1
y2 <= 1
y3 <= 1
'''
    Prob('1.18', prob)


def test2():
    prob = '''
max 2*x1 + x2

5*x2 <= 15
6*x1 + 2*x2 <= 24
x1 + x2 <= 5
x1 >= 0
x2 >= 0
'''
    Prob('', prob)

def test3():
    Prob('', '''
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


test1()
