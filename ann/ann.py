import numpy as np

def load_txt(fname):
    with open(fname) as f:
        for _ in range(5):
            f.readline()
        return np.matrix(f.read().strip().replace('\n', ';'))

'''
X = load('X.txt')
y = load('y.txt')
theta1 = load('theta1.txt')
theta2 = load('theta2.txt')

np.save('X.npy', X)
np.save('y.npy', y)
np.save('theta1.npy', theta1)
np.save('theta2.npy', theta2)
'''

def load(fname):
    return np.matrix(np.load(fname))


X = load('data/X.npy')
y = load('data/y.npy')
theta1 = load('data/theta1.npy')
theta2 = load('data/theta2.npy')


def sigmoid(z):
    return 1. / (1. + np.exp(-z))

def sigmoidGradient(z):
    return np.multiply(sigmoid(z), 1-sigmoid(z))


def nnCostFunction(theta1,
    theta2,
    input_layer_size,
    hidden_layer_size,
    num_labels,
    X,
    y,
    lambda_):
    '''
    the neural network cost function for a two layer neural network
    J, grad = nnCostFunction(...)
    '''
    m = X.shape[0]
    J = 0
    theta1_grad = np.zeros(theta1.shape)
    theta2_grad = np.zeros(theta2.shape)

    for i in range(m):
        a1 = np.vstack(([1], X[i,:].T))

        z2 = theta1 * a1
        a2 = np.vstack(([1], sigmoid(z2)))

        z3 = theta2 * a2
        a3 = sigmoid(z3)

        h = a3

        yi = np.zeros((num_labels, 1))
        tmp = y[i,0]
        if tmp == 10:
            tmp = 0
        yi[tmp] = 1

        J -= (yi.T * np.log(h) + (1-yi).T * np.log(1-h))

        d3 = a3 - yi

        d2 = np.multiply((theta2.T * d3)[1:], sigmoidGradient(z2))

        theta1_grad += d2 * a1.T
        theta2_grad += d3 * a2.T

    J += .5 * lambda_ * (np.square(theta1[:,1:]).sum() + np.square(theta2[:,1:]).sum())
    J /= m

    theta1_grad = (theta1_grad + np.hstack((np.zeros((theta1.shape[0], 1)), lambda_ * theta1[:,1:]))) / m
    theta2_grad = (theta2_grad + np.hstack((np.zeros((theta2.shape[0], 1)), lambda_ * theta2[:,1:]))) / m

    return J, (theta1_grad, theta2_grad)


def ex4():
    input_layer_size = 400
    hidden_layer_size = 25
    num_labels = 10
    lambda_ = 0

    J, grad = nnCostFunction(theta1, theta2,
        input_layer_size, hidden_layer_size,
        num_labels, X, y, lambda_)

    print J


if __name__ == '__main__':
    ex4()
