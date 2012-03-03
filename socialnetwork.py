import math
from PIL import Image, ImageDraw


people = C,A,Ve,Vi,Mk,J,W,Mr = ['Charlie', 'Augustus', 'Veruca', 'Violet', 'Mike', 'Joe', 'Willy', 'Miranda']

links = [
    (A, W),
    (Mk, J),
    (Mr, Mk),
    (Vi, A),
    (Mr, W),
    (C, Mk),
    (Ve, J),
    (Mr, A),
    (W, A),
    (J, C),
    (Ve, A),
    (Mr, J),
    ]


def crosscount(v):
    loc = dict([(people[i],(v[i*2],v[i*2+1]))
        for i in range(len(people))])
    total = 0

    for i in range(len(links)):
        for j in range(i+1, len(links)):
            (x1, y1), (x2, y2) = loc[links[i][0]], loc[links[i][1]] 
            (x3, y3), (x4, y4) = loc[links[j][0]], loc[links[j][1]] 

            den = (y4-y3) * (x2-x1) - (x4-x3) * (y2-y1)
            if den == 0:
                continue

            ua = ((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/float(den)
            ub = ((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/float(den)
            if ua>0 and ua<1 and ub>0 and ub<1:
                total += 1

    min_, max_ = 50., 250.
    for i in range(len(people)):
        for j in range(i+1, len(people)):
            (x1,y1), (x2,y2) = loc[people[i]], loc[people[j]]
            dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
            if dist < min_:
                total += (1. - dist/min_)
            elif dist > max_:
                total += (1. - max_/dist)


    def cosv(v1, v2):
        def dotp(v1, v2):
            return v1[0]*v2[0] + v1[1]*v2[1]
        def module(v):
            return math.sqrt(v[0]**2 + v[1]**2)
        try:
            return dotp(v1, v2) / (module(v1) * module(v2))
        except ZeroDivisionError:
            return 1

    def edgev(e):
        def vector(p1, p2):
            return p2[0]-p1[0], p2[1]-p1[1]
        return vector(loc[e[0]], loc[e[1]])

    small_angle = 90
    threshold = math.cos(small_angle*math.pi/180)
    for vertex, (x, y) in loc.items():
        edges = [ ((from_, to) if from_ == vertex else (to, from_))
             for from_, to in links if vertex in (from_, to) ]
        for i in range(len(edges)):
            for j in range(i+1, len(edges)):
                e1, e2 = edges[i], edges[j]
                cos = cosv(edgev(e1), edgev(e2))
                if cos > threshold:
                    total += (cos-threshold)*5

    return total

def draw_network(sol):
    img = Image.new('RGB', (400,400), (255,255,255))
    draw = ImageDraw.Draw(img)
    pos = dict([(people[i], (sol[i*2],sol[i*2+1]))
        for i in range(len(people))])
    for (a,b) in links:
        draw.line((pos[a], pos[b]), fill=(255,0,0))
    for n,p in pos.items():
        draw.text(p,n,(0,0,0))
    img.show()

if __name__ == '__main__':
    domain = [(10,370)]*(len(people)*2)

    import optimization as opt
    best, sol = opt.run(opt.random_optimize, domain, crosscount, 5)
    print best
    draw_network(sol)
