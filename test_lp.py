import unittest
import lp
from lp import extract_var, solve

class ExtractVarTest(unittest.TestCase):

    def test_empty(self):
        for ex in ['', '1', '1+2', '1+3>2']:
            self.assertEquals(0, len(extract_var(ex)))

    def test_basic(self):
        self.assertEquals(set(['x']), extract_var('x'))
        self.assertEquals(set(['x']), extract_var('x+x'))
        self.assertEquals(set(['x', 'y']), extract_var('x+y'))
        self.assertEquals(set(['x', 'y']), extract_var('x+1==y'))


prob1 = '''
min x
#cat Integer

x - 100 - w1 - w2 == y1
1.04*y1 - 150 - w3 == y2
1.04*y2 - 120 + 1.25*w2 == y3
1.04*y3 + 1.4*w1 + 1.3*w3 == 110
w1 <= 60
w2 <= 90
w3 <= 50
x,y1,y2,y3,w1,w2,w3 >= 0
'''

prob2 = '''
max 2*x1 + x2

5*x2 <= 15
6*x1 + 2*x2 <= 24
x1 + x2 <= 5
x1,x2 >= 0
'''

prob3 = '''
max 2*x1 + 3*x2 + x3

x1 + x3 == 5
x1 + 2*x2 + x4 == 10
x2 + x5 == 4
x1 >= 0
x2 >= 0
x3 >= 0
x4 >= 0
x5 >= 0
'''

prob4 = '''
max 27*x1 + 21*x2 - 10*x1 - 9*x2 - 14*x1 - 10*x2

2*x1 + x2 <= 100
x1 + x2 <= 80
x1 <= 40
x1,x2 >= 0
'''


def smoking():
    solve(prob1)

if __name__ == '__main__':
    #unittest.main()
    smoking()
