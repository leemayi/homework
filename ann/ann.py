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


def nnCostFunction(nn_params,
    input_layer_size,
    hidden_layer_size,
    num_labels,
    X,
    y,
    lambda_):

    num = hidden_layer_size * (input_layer_size+1)
    theta1 = nn_params[:num].reshape((hidden_layer_size, input_layer_size+1))
    theta2 = nn_params[num:].reshape((num_labels, hidden_layer_size+1))

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
            tmp = 9
        else:
            tmp -= 1
        yi[tmp] = 1

        J -= (yi.T * np.log(h) + (1-yi).T * np.log(1-h))[0,0]

        d3 = a3 - yi

        d2 = np.multiply((theta2.T * d3)[1:], sigmoidGradient(z2))

        theta1_grad += d2 * a1.T
        theta2_grad += d3 * a2.T

    J += lambda_ * (np.square(theta1[:,1:]).sum() + np.square(theta2[:,1:]).sum()) / 2.
    J /= m

    theta1_grad = (theta1_grad + np.hstack((np.zeros((theta1.shape[0], 1)), lambda_ * theta1[:,1:]))) / m
    theta2_grad = (theta2_grad + np.hstack((np.zeros((theta2.shape[0], 1)), lambda_ * theta2[:,1:]))) / m

    return J, np.hstack((theta1_grad.flatten(), theta2_grad.flatten())).T


def randInitializeWeights(L_in, L_out):
    #epsilon_init = 6 ^ .5 / (L_out + L_in) ^ .5
    epsilon_init = 0.12
    return np.matrix(np.random.rand(L_out, 1 + L_in) * 2 * epsilon_init - epsilon_init)


def max_index(v):
    max_idx = 0
    max_ = v[0]
    for i in range(v.size):
        if v[i] > max_:
            max_ = v[i]
            max_ix = i
    return max_idx


def predict(theta1, theta2, X):
    m = X.shape[0]
    num_labels = theta2.shape[0]

    h1 = sigmoid(np.hstack((ones((m, 1)), X)) * theta1.T)
    h2 = sigmoid(np.hstack((ones((m, 1)), h1)) * theta2.T)
    return max_index(h2)


def fmin(costFunction, initial, alpha=.3, maxiter=50):
    theta = initial
    for i in range(maxiter):
        J, grad = costFunction(theta)
        if small_enough(grad):
            break
        theta -= alpha * grad
    return theta, J


def ex4():
    input_layer_size = 400
    hidden_layer_size = 25
    num_labels = 10
    lambda_ = 1
    nn_params = np.hstack((theta1.flatten(), theta2.flatten())).T

    J, grad = nnCostFunction(nn_params,
        input_layer_size, hidden_layer_size,
        num_labels, X, y, lambda_)

    print J

    g = sigmoidGradient(np.array([1,-.5,0,.5,1]))
    print g



if __name__ == '__main__':
    ex4()
