from mat import Mat
import math

## Task 1
def identity(labels = {'x','y','u'}):
    '''
    In case you have never seen this notation for a parameter before,
    the way it works is that identity() now defaults to having labels 
    equal to {'x','y','u'}.  So you should write your procedure as if 
    it were defined 'def identity(labels):'.  However, if you want the labels of 
    your identity matrix to be {'x','y','u'}, you can just call 
    identity().  Additionally, if you want {'r','g','b'}, or another set, to be the
    labels of your matrix, you can call identity({'r','g','b'}).  
    '''
    return Mat((labels, labels),
        { (r,c):1 for r in labels for c in labels if r == c })

## Task 2
def translation(x,y):
    '''
    Input:  An x and y value by which to translate an image.
    Output:  Corresponding 3x3 translation matrix.
    '''
    return Mat(({'x','y','u'}, {'x','y','u'}), {
        ('x','x'): 1,
        ('y','y'): 1,
        ('u','u'): 1,
        ('x','u'): x,
        ('y','u'): y,
        })

## Task 3
def scale(a, b):
    '''
    Input:  Scaling parameters for the x and y direction.
    Output:  Corresponding 3x3 scaling matrix.
    '''
    d = {'x','y','u'}
    return Mat((d,d), {
        ('x','x'): a,
        ('y','y'): b,
        ('u','u'): 1,
        })

## Task 4
def rotation(angle):
    '''
    Input:  An angle in radians to rotate an image.
    Output:  Corresponding 3x3 rotation matrix.
    Note that the math module is imported.
    '''
    d = {'x','y','u'}
    _cos = math.cos(angle)
    _sin = math.sin(angle)
    return Mat((d,d), {
        ('x','x'): _cos,
        ('x','y'): -_sin,
        ('y','x'): _sin,
        ('y','y'): _cos,
        ('u','u'):1,
        })

## Task 5
def rotate_about(x,y,angle):
    '''
    Input:  An x and y coordinate to rotate about, and an angle
    in radians to rotate about.
    Output:  Corresponding 3x3 rotation matrix.
    It might be helpful to use procedures you already wrote.
    '''
    return translation(x,y)*rotation(angle)*translation(-x,-y)

## Task 6
def reflect_y():
    '''
    Input:  None.
    Output:  3x3 Y-reflection matrix.
    '''
    d = {'x','y','u'}
    return Mat((d,d), {
        ('x','x'): -1,
        ('y','y'): 1,
        ('u','u'): 1,
        })

## Task 7
def reflect_x():
    '''
    Inpute:  None.
    Output:  3x3 X-reflection matrix.
    '''
    d = {'x','y','u'}
    return Mat((d,d), {
        ('x','x'): 1,
        ('y','y'): -1,
        ('u','u'): 1,
        })
    
## Task 8    
def scale_color(scale_r,scale_g,scale_b):
    '''
    Input:  3 scaling parameters for the colors of the image.
    Output:  Corresponding 3x3 color scaling matrix.
    '''
    d = {'r','g','b'}
    return Mat((d,d), {
        ('r','r'): scale_r,
        ('g','g'): scale_g,
        ('b','b'): scale_b,
        })

## Task 9
def grayscale():
    '''
    Input: None
    Output: 3x3 greyscale matrix.
    '''
    d = {'r','g','b'}
    r, g, b = 77/256, 151/256, 28/256
    return Mat((d,d), {
        ('r','r'): r,
        ('r','g'): g,
        ('r','b'): b,
        ('g','r'): r,
        ('g','g'): g,
        ('g','b'): b,
        ('b','r'): r,
        ('b','g'): g,
        ('b','b'): b,
        })

## Task 10
def reflect_about(p1,p2):
    '''
    Input: 2 points that define a line to reflect about.
    Output:  Corresponding 3x3 reflect about matrix.
    '''
    (x1,y1), (x2,y2) = p1, p2
    theta = math.atan2(y1-y2, x1-x2)
    return \
        translation(x1,y1) * \
        rotation(theta) * \
        reflect_x() * \
        rotation(-theta) * \
        translation(-x1,-y1)


