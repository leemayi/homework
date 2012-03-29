#coding: utf8

def mid_order(r):
    stack = []
    p = r
    while 1:
        while p:
            stack.append(p)
            p = p.left
        if not stack:
            break
        p = stack.pop()
        yield p.data
        p = p.right

def pre_order(r):
    stack = []
    p = r
    while 1:
        while p:
            yield p.data
            stack.append(p)
            p = p.left
        if not stack:
            break
        p = stack.pop()
        p = p.right

def post_order(r):
    stack = []
    p = r
    while 1:
        while p:
            pass
        


class N(object):

    def __init__(self, data, left=None, right=None):
        self.data, self.left, self.right = data, left, right

    def __str__(self):
        return str(self.data)

r = N(1, N(2, N(4), N(5)), N(3))

print ' '.join([str(i) for i in mid_order(r)])
print ' '.join([str(i) for i in pre_order(r)])
