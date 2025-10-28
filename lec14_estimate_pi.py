import random
import math

checkpoint_steps = 1000
def estimate_pi(num_samples=1000000):
    points_sum = 0
    checkpoints = []
    for i in range(1, num_samples+1):
        x = random.random()
        y = random.random()
        if x*x+y*y<1:
            points_sum += 1

        if i % checkpoint_steps == 0:
            checkpoints.append(4*points_sum/i)
            print("Samples:", i, "Estimate:", 4*points_sum/i, end="                               \r")
    print()
    return 4*points_sum/i, checkpoints

def estimate_pi_biased(num_samples=1000000):
    points_sum = 0
    checkpoints = []
    for i in range(1, num_samples+1):
        x = random.random()
        y = random.random()
        if y > 0.9:
            y = random.random()
        if x*x+y*y<1:
            points_sum += 1

        if i % checkpoint_steps == 0:
            checkpoints.append(4*points_sum/i)
            print("Samples:", i, "Estimate:", 4*points_sum/i, end="                               \r")
    print()
    return 4*points_sum/i, checkpoints

def estimate_pi_high_variance(num_samples=1000000):
    points_sum = 0
    checkpoints = []
    for i in range(1, num_samples+1):
        x = random.random() * 10
        y = random.random() * 10
        if x*x+y*y<1:
            points_sum += 1

        if i % checkpoint_steps == 0:
            checkpoints.append(400*points_sum/i)
            print("Samples:", i, "Estimate:", 400*points_sum/i, end="                               \r")
    print()
    return 400*points_sum/i, checkpoints

print("Estimate pi:")
_, c1 = estimate_pi()
print("\nEstimate pi with a slight sampling bias:")
_, c2 = estimate_pi_biased()
print("\nEstimate pi with a high sampling variance:")
_, c3 = estimate_pi_high_variance()
print("\nEstimate pi with a high sampling variance but many simulations:")
_, c4 = estimate_pi_high_variance(100000000)

import matplotlib.pyplot as plt

bg_color = (250/255, 245/255, 235/255)
plt.rcParams.update({
    "figure.facecolor" : bg_color,
    "axes.facecolor" : bg_color,
    "font.size" : 14,
    "ytick.labelsize" : 12,
    "figure.figsize" : (10,6)
})

x_vals = [i*checkpoint_steps for i in range(1, len(c1)+1)]
plt.plot(x_vals, [math.pi for _ in c1], label="Pi", linewidth=2)
plt.plot(x_vals, c1, label="Normal estimate", linewidth=2)
plt.plot(x_vals, c2, label="Biased estimate", linewidth=2)
plt.plot(x_vals, c3, label="High variance estimate", linewidth=2)

plt.title("Estimation of Pi by Monte Carlo sampling")
plt.xlabel("Sample number")
plt.ylabel("Pi estimate")
plt.ylim(3, 3.4)
plt.legend()
plt.grid()
plt.savefig("estimate_pi.png")