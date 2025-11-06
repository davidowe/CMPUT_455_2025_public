import random
import numpy as np

def mean_squared_error(data, f):
    return sum([(f(x)-y)**2 for x, y in data])

def gradient_descent_iteration(data, f, f_prime, theta, alpha):
    mse_grad = sum([(y-f(theta, x))*f_prime(theta, x) for x, y in data])
    theta -= alpha * ((-2)/len(data)) * mse_grad
    return theta

to_approximate = lambda x: 0.4*(x**3)

data = [(x, to_approximate(x)) for x in [random.random() for i in range(10)]]

theta = 5
f = lambda theta, x: theta*(x**3)
f_prime = lambda theta, x: theta*3*(x**2)
alpha = 0.1
for i in range(100):
    theta = gradient_descent_iteration(data, f, f_prime, theta, alpha)
print("Theta:", theta, "MSE:", sum([(y-f(theta,x))**2 for x, y in data]))

def neural_network(x, W, b, g):
    a = x
    for l in range(len(W)):
        a = g[l](b[l] + np.matmul(W[l], a))
    return a

def ReLU(x):
    return x if x > 0 else 0

x = np.array([1,2])
W = [\
    np.array([[2,1.5],[0.5,-2.5],[1,-0.5]]),\
    np.array([[2,-4.5,1],[-1,0.5,0.5]]),\
    np.array([[0.5,2]])
    ]
b = [np.array([0.5,-3,2]),np.array([2,4]),np.array([3])]
g = [np.vectorize(ReLU)]*3

print(neural_network(x, W, b, g))