import numpy as np

class SlotMachine:
    def __init__(self, mean=None, std_dev=None):
        self.mean = mean
        self.std_dev = std_dev
        if mean is None:
            self.mean = np.random.normal(scale=2)
        if std_dev is None:
            self.std_dev = (1 + abs(np.random.normal())) * 2
        self.payout_history = []
        self.observed_mean = None
        self.observed_var = None
        
    def play(self):
        payout = round(np.random.normal(loc=self.mean, scale=self.std_dev),2)
        self.payout_history.append(payout)
        self.observed_mean = sum(self.payout_history)/len(self.payout_history)
        self.observed_var = sum([(x - self.observed_mean)**2 for x in self.payout_history])/len(self.payout_history)
        return payout

    def print_observed(self):
        print("From the observed payout history of:", ", ".join([str(round(x,2)) for x in self.payout_history]))
        print("The observed mean is:", round(self.observed_mean, 2))
        print("The observed variance is:", round(self.observed_var))

def print_val(val):
    if val is None:
        return "None"
    else:
        return str(round(val,2))

num_machines = int(input("Enter the number of slot machines:"))  
print("Enter -1 to end the game and see the true machine means and variances.")  
machines = [SlotMachine() for i in range(num_machines)]

for i, machine in enumerate(machines):
    print("Machine", i, ": observed mean =", print_val(machine.observed_mean), "\tobserved var =", print_val(machine.observed_var), "\tpast payouts =", ", ".join([str(round(x,2)) for x in machine.payout_history]))
print()

total_payout = 0
num_plays = 0
while True:
    m = int(input("Enter the machine number to play:"))
    if m < 0:
        break
    if m >= len(machines):
        print("Invalid machine number try again.")
        continue
    print("\nPlaying machine", m)
    payout = machines[m].play()
    total_payout += payout
    num_plays += 1
    print("Payout:", payout)
    print("Total payout so far:", total_payout, "from", num_plays, "plays, average payout:", total_payout/num_plays)
    print()
    for i, machine in enumerate(machines):
        print("Machine", i, ": observed mean =", print_val(machine.observed_mean), "\tobserved var =", print_val(machine.observed_var), "\tpast payouts =", ", ".join([str(round(x,2)) for x in machine.payout_history]))
    print()
    
for i, machine in enumerate(machines):
    print("Machine", i, ": true mean =", print_val(machine.mean), "\ttrue var =", print_val(machine.std_dev**2))