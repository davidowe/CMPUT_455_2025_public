import random
import math

# Estimates the definite integral of f from x0 to x1
# 0 <= f(x) <= max_y must be true for all x in [x0,x1]
def est_integral(f, x0, x1, max_y, num_samples=100000):
    x_dist = x1-x0
    total_area = x_dist*max_y
    points_sum = 0
    for i in range(num_samples):
        x = x0 + random.random()*x_dist
        y = random.random()*max_y
        if y < f(x):
            points_sum += 1
    return total_area * points_sum / num_samples

print(est_integral(lambda x: 2*math.sin(x/3)+5, -1, 2, 7, 1000000))

def sum_decimal_digits(x):
    s = str(x - int(x))[2:5]
    return sum([int(c) for c in s]) / (9 * len(s))

print(est_integral(sum_decimal_digits, 10, 15, 1, 1000000))