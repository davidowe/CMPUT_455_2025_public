import numpy as np
import math

def ReLU(x):
    return x if x > 0 else 0.1*x

def ReLU_prime(x):
    return 1 if x > 0 else 0.1

class NeuralNetwork:
    def __init__(self, layers_sizes, learning_rate=0.1):
        self.learning_rate = learning_rate
        self.W = []
        self.b = []
        self.g = []
        self.g_prime = []
        for i in range(1, len(layers_sizes)):
            self.W.append(np.array(np.random.normal(loc=0, size=(layers_sizes[i], layers_sizes[i-1]))))
            self.b.append(np.array(np.random.normal(loc=0, size=(layers_sizes[i]))))
            self.g.append(np.vectorize(ReLU))
            self.g_prime.append(np.vectorize(ReLU_prime))

    #returns output, bias derivaties, and weight derivatives
    def backpropagate(self, x):
        #Forward pass:
        z = []
        a = [x]
        for l in range(len(self.W)):
            z.append(self.b[l]+np.matmul(self.W[l], a[l]))
            a.append(self.g[l](z[l]))

        #Calculate derivatives:
        W_prime = [np.zeros(self.W[l].shape) for l in range(len(self.W))]
        delta   = [np.zeros(self.b[l].shape) for l in range(len(self.b))] #doubles as b_prime
        for l in range(len(self.W)-1, -1, -1): #From the last to first hidden layer
            if l == len(self.W)-1:
                delta[l] = self.g_prime[-1](z[-1])
            else:
                delta[l] = self.g_prime[l](z[l])*np.matmul(delta[l+1].T, self.W[l+1])
            for i in range(self.W[l].shape[0]): #For each neuron of the current layer
                for j in range(self.W[l].shape[1]): #For each neuron of the last layer
                    W_prime[l][i][j] = delta[l][i] * a[l][j]

        return a[-1], delta, W_prime
    
    def mean_squared_error(self, data_points):
        error = 0
        for x, y in data_points:
            a = x
            for l in range(len(self.W)):
                a = self.g[l](self.b[l] + np.matmul(self.W[l], a))
            error += (y - a)**2
        return error / len(data_points)

    def gradient_descent(self, data_points):
        W_err = [np.zeros(self.W[l].shape) for l in range(len(self.W))]
        b_err = [np.zeros(self.b[l].shape) for l in range(len(self.b))]
        for x, y in data_points:
            output, b_prime, W_prime = self.backpropagate(x)
            err = (y - output)[0]
            for l in range(len(self.W)):
                b_err[l] += err * b_prime[l]
                W_err[l] += err * W_prime[l]
                
        for l in range(len(self.W)):
            self.W[l] = self.W[l] + self.learning_rate * W_err[l] / len(data_points)
            self.b[l] = self.b[l] + self.learning_rate * b_err[l] / len(data_points)

def hidden_func(x):
    return  3*math.cos(1+0.5*x)*(math.sin(x)-0.25)**2+np.random.normal(loc=0)

def generate_data(num_samples):
    data_points = []
    for i in num_samples:
        x = np.random.normal()
        y = hidden_func(x)
        data_points.append((np.array([x]), np.array([y])))
    return data_points

training_data_points = generate_data(1000)
testing_data_points = generate_data(1000)
nn = NeuralNetwork([1, 5, 5, 5, 5, 1], 0.01)
mse_list = []
num_steps = 200
for i in range(num_steps):
    nn.gradient_descent(training_data_points)
    mse_list.append(nn.mean_squared_error(testing_data_points))

    #print("MSE:", mse)
import matplotlib.pyplot as plt

bg_color = (250/255, 245/255, 235/255)
plt.rcParams.update({
    "figure.facecolor" : bg_color,
    "axes.facecolor" : bg_color,
    "font.size" : 14,
    "ytick.labelsize" : 12,
    "figure.figsize" : (10,6)
})

plt.plot([i for i in range(1, num_steps+1)], mse_list, linewidth=2)

plt.title("MSE of a neural network during gradient descent")
plt.xlabel("Step")
plt.ylabel("MSE")
plt.grid()
plt.savefig("nn_mse.png")

plt.clf()
plt.plot([i for i in range(25, num_steps+1)], mse_list[24:], linewidth=2)

plt.title("MSE of a neural network during gradient descent")
plt.xlabel("Step")
plt.ylabel("MSE")
plt.grid()
plt.savefig("nn_mse2.png")