from sympy import *
from sympy import abc


def hr(msg):
    for i in range(7):
        print
    print ' '*10, msg
    print

def sigmoid(z):
    return 1 / (1 + abc.e ** -z)

m = 1
y, z = symbols(['y', 'z'])
x = symbols(['1', 'x'])
theta = symbols(['t0', 't1'])

theta_x = 0
for i, j in zip(theta, x):
    theta_x += i * j

h = sigmoid(theta_x)
hr('h')
pprint(h)

J = (-1/m) * (y * ln(h) + (1 - y) * ln(1 - h))
hr('J')
pprint(J)
d0 = diff(J, theta[0])
d1 = diff(J, theta[1])

hr('diff(J, theta0)')
pprint(d0)

hr('diff(J, theta1)')
pprint(d1)
pprint(d1.expand())
