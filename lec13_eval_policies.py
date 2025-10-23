import numpy as np
import random
import math

class SlotMachine:
    def __init__(self, mean=None, std_dev=None):
        self.mean = mean
        self.std_dev = std_dev
        if mean is None:
            self.mean = np.random.normal(scale=4)
        if std_dev is None:
            self.std_dev = (1 + abs(np.random.normal())) * 20
        self.payout_history = []
        self.observed_mean = None
        self.observed_var = None
        self.plays = 0
        
    def play(self):
        self.plays += 1
        payout = round(np.random.normal(loc=self.mean, scale=self.std_dev),2)
        self.payout_history.append(payout)
        self.observed_mean = sum(self.payout_history)/len(self.payout_history)
        self.observed_var = sum([(x - self.observed_mean)**2 for x in self.payout_history])/len(self.payout_history)
        return payout

    def print_observed(self):
        print("From the observed payout history of:", ", ".join([str(round(x,2)) for x in self.payout_history]))
        print("The observed mean is:", round(self.observed_mean, 2))
        print("The observed variance is:", round(self.observed_var))

num_machines = 16
num_plays = 32
num_samples = 1000

def uniform_then_greedy_factory(n):
    def uniform_then_greedy(machines):
        max_i = 0
        max_mean = -float('inf')
        for i, m in enumerate(machines):
            if m.plays < n:
                return i
            if m.observed_mean > max_mean:
                max_mean = m.observed_mean
                max_i = i
        return max_i
    return uniform_then_greedy

def epsilon_greedy_factory(n):
    def epsilon_greedy(machines):
        if random.random() < n:
            return random.randint(0,len(machines)-1)
        max_mean = -float('inf')
        max_i = 0
        for i, m in enumerate(machines):
            if m.observed_mean is not None and m.observed_mean > max_mean:
                max_mean = m.observed_mean
                max_i = i
        return max_i
    return epsilon_greedy

def UCB_factory(n):
    def UCB_formula(x, c, plays, total_plays):
        return x+c*math.sqrt(math.log(total_plays)/plays)
    
    def UCB_selection(machines):
        total_plays = sum([m.plays for m in machines])
        max_ucb = -float('inf')
        max_i = 0
        for i, m in enumerate(machines):
            if m.observed_mean is None:
                return i
            ucb_i = UCB_formula(m.observed_mean, n, m.plays, total_plays)
            if ucb_i > max_ucb:
                max_ucb = ucb_i
                max_i = i
        return max_i

    return UCB_selection

def sequential_halving(machines, num_plays=64):
    num_rounds = math.ceil(math.log2(len(machines)))
    round_budget = num_plays // num_rounds
    considered = list(machines)
    for i, m in enumerate(considered):
        m.id = i
    total_played = 0
    to_play_index = 0
    while total_played < num_plays:
        considered[to_play_index].play()
        total_played += 1
        to_play_index = (to_play_index + 1) % len(considered)
        if total_played % round_budget == 0 and len(considered) > 2:
            to_play_index = 0
            considered.sort(key=lambda x:x.observed_mean if x.observed_mean is not None else -float('inf'), reverse=True)
            considered = considered[:len(considered)//2]
    return considered[0].id \
           if considered[0].observed_mean > considered[1].observed_mean \
           else considered[1].id

policies =  [uniform_then_greedy_factory(i) for i in range(1, int(num_plays/num_machines)+1)]+\
            [epsilon_greedy_factory(i/int(num_plays/num_machines)) for i in range(int(num_plays/num_machines))]+\
            [UCB_factory(30*x/int(num_plays/num_machines)) for x in range(1, int(num_plays/num_machines)+1)]
policy_labels = [str(i*num_machines)+" uniform then greedy" for i in range(1, int(num_plays/num_machines)+1)]+\
                [str(i)+" Epsilon greedy" for i in range(num_machines, num_plays+1, num_machines)]+\
                ["UCB with constant "+str(30*x/int(num_plays/num_machines)) for x in range(1, int(num_plays/num_machines)+1)]


cumulative_regret = [0]*len(policies)
simple_regret = [0]*len(policies)

for sample in range(num_samples):
    if sample % 10 == 0:
        print(sample / num_samples, end='      \r')
    base_machines = [SlotMachine() for i in range(num_machines)]
    base_machines2 = [SlotMachine() for i in range(num_machines)]
    for i in range(len(policies)):
        policy = policies[i]
        machines = [SlotMachine(x.mean, x.std_dev) for x in base_machines]
        best_mean = max([x.mean for x in machines])
        for play in range(num_plays):
            #if play == (num_plays//2):
            #    for j in range(len(machines)):
            #        machines[j].mean = base_machines2[j].mean
            #        machines[j].std_dev = base_machines2[j].std_dev
            #        best_mean = max([x.mean for x in machines])
            choice = policy(machines)
            #print("choice")
            machines[choice].play()
            cumulative_regret[i] += best_mean - machines[choice].mean
        simple_regret[i] += best_mean - max([(m.mean, m.observed_mean) if m.observed_mean is not None else (m.mean, -float('inf')) for m in machines], key=lambda x:x[1])[0]

for i in range(len(policies)):
    print("Policy:", policy_labels[i])
    cumulative_regret[i] /= num_samples
    print("Average cumulative regret:", cumulative_regret[i])
    print()

import matplotlib.pyplot as plt

bg_color = (250/255, 245/255, 235/255)
plt.rcParams.update({
    "figure.facecolor" : bg_color,
    "axes.facecolor" : bg_color,
    "font.size" : 14,
    "ytick.labelsize" : 12,
    "figure.figsize" : (10,6)
})

x_points = [i/int(num_plays/num_machines) for i in range(1,1+int(num_plays/num_machines))]
uniform_p = cumulative_regret[:len(x_points)]
random_p = cumulative_regret[len(x_points):2*len(x_points)]
ucb_p = cumulative_regret[2*len(x_points):]
plt.plot(x_points, uniform_p, label="Uniform then greedy")
plt.plot(x_points, random_p, label="Epsilon greedy")
plt.plot(x_points, ucb_p, label="UCB")
plt.legend()
plt.title("Cumulative Regret from multiple policies")
plt.xlabel("Adjustable parameter values")
plt.ylabel("Cumulative Regret")
plt.savefig("cumulative_multiarm_bandit_policies.png")

sh_simple_regret = 0
for sample in range(num_samples):
    machines = [SlotMachine() for i in range(num_machines)]
    best_mean = max([x.mean for x in machines])
    choice = sequential_halving(machines, num_plays)
    sh_simple_regret += best_mean - machines[choice].mean
sh_simple_regret /= num_samples

for i in range(len(policies)):
    print("Policy:", policy_labels[i])
    simple_regret[i] /= num_samples
    print("Average simple regret:", simple_regret[i])
    print()
print("Policy: Sequential Halving")
print("Average simple regret:", sh_simple_regret)
print()

plt.clf()
uniform_p = simple_regret[:len(x_points)]
random_p = simple_regret[len(x_points):2*len(x_points)]
ucb_p = simple_regret[2*len(x_points):]
sh_p = [sh_simple_regret]*len(x_points)
plt.plot(x_points, uniform_p, label="Uniform then greedy")
plt.plot(x_points, random_p, label="Epsilon greedy")
plt.plot(x_points, ucb_p, label="UCB")
plt.plot(x_points, sh_p, label="Sequential Halving")
plt.legend()
plt.title("Simple Regret from multiple policies")
plt.xlabel("Adjustable parameter values")
plt.ylabel("Simple Regret")
plt.savefig("simple_multiarm_bandit_policies.png")