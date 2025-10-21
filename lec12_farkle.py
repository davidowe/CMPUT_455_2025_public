score_tt = {}
#returns score, num dice remaining
def score_dice(dice):
    global score_tt
    counts = [0] * 6
    for roll in dice:
        counts[roll-1] += 1
    if counts == [1, 1, 1, 1, 1, 1]:
        return 1500, 6
    key = str(counts)
    if key in score_tt:
        return score_tt[key][0], score_tt[key][1]
    num_triples = 0
    num_pairs = 0
    largest_of_a_kind = 0
    triple_num = 0
    num_ones = counts[0]
    num_fives = counts[4]
    
    for i, count in enumerate(counts):
        if count > largest_of_a_kind:
            largest_of_a_kind = count
        if count == 2:
            num_pairs += 1
        if count == 3:
            num_triples += 1
            triple_num = i+1

    if num_triples == 2:
        score_tt[key] = (2500, 6)
        return 2500, 6
    if num_pairs == 3 or (num_pairs == 1 and largest_of_a_kind == 4):
        score_tt[key] = (1500, 6)
        return 1500, 6
    
    score = 0
    num_dice = len(dice)
    if largest_of_a_kind >= 4:
        score += 1000 * (largest_of_a_kind-3)
        num_dice -= largest_of_a_kind
    if num_triples == 1 and triple_num != 1:
         score += 100 * triple_num
         num_dice -= 3
    if num_ones <= 3:
        score += 100*num_ones
        num_dice -= num_ones
    if num_fives < 3:
        score += 50*num_fives
        num_dice -= num_fives
    if score == 0:
        num_dice = 0
    elif num_dice == 0:
        num_dice = 6
    score_tt[key] = (score, num_dice)
    return score, num_dice

# Takes a list of dice values, and the dice index currently being modified
def compute_one_roll_EV(dice, dice_index):
    if dice_index == len(dice): # All dice are set
        score, _ = score_dice(dice)
        return score, 1 if score == 0 else 0 # Return the score and whether it was a Farkle
    value_sum = 0
    farkle_rolls = 0
    for i in range(6):
        dice[dice_index] = i+1 # Set one of the dice values
        value_sum_child, farkle_rolls_child = compute_one_roll_EV(dice, dice_index+1)
        value_sum += value_sum_child / 6
        farkle_rolls += farkle_rolls_child / 6
    return value_sum, farkle_rolls

roll_EV = []
roll_F_prob = []
for i in range(6):
    print("Computing results for one roll of", i+1, "dice:")
    value_sum, farkle_rolls = compute_one_roll_EV([1]*(i+1), 0)
    print("Expected value:", value_sum)
    print("Farkle chance:", farkle_rolls)
    roll_EV.append(value_sum)
    roll_F_prob.append(farkle_rolls)

def compute_over_all_rolls_policy(dice, depth, turn_score, policy, tt):
    if depth == len(dice):
        return compute_policy_EV(dice, turn_score, policy, tt)
    ev = 0
    child_dice = list(dice)
    for i in range(6):
        child_dice[depth] = i+1
        ev += compute_over_all_rolls_policy(child_dice, depth+1, turn_score, policy, tt) / 6
    return ev

def compute_policy_EV(dice, turn_score, policy, tt):
    roll_score, num_dice = score_dice(dice)
    if roll_score == 0:
        return 0
    else:
        turn_score += roll_score
    if turn_score >= 10000:
        return 10000
    if not policy(num_dice, turn_score):
        return turn_score
    key = str(num_dice) + "," + str(turn_score)
    if key in tt:
        return tt[key]
    child_dice = [1] * num_dice
    result = compute_over_all_rolls_policy(child_dice, 0, turn_score, policy, tt)
    tt[key] = result
    return result

def compute_over_all_rolls_optimal(dice, depth, turn_score, policy, tt):
    if depth == len(dice):
        return compute_optimal_policy(dice, turn_score, policy, tt)
    ev = 0
    child_dice = list(dice)
    for i in range(6):
        child_dice[depth] = i+1
        ev += compute_over_all_rolls_optimal(child_dice, depth+1, turn_score, policy, tt) / 6
    return ev

def compute_optimal_policy(dice, turn_score, policy, tt):
    roll_score, num_dice = score_dice(dice)
    if roll_score == 0:
        return 0
    else:
        turn_score += roll_score
    if turn_score >= 10000:
        return 10000
    
    key = str(num_dice) + "," + str(turn_score)
    if key in tt:
        return tt[key]
    
    child_dice = [1] * num_dice
    ev_reroll = compute_over_all_rolls_optimal(child_dice, 0, turn_score, policy, tt)
    policy[key] = ev_reroll > turn_score # True = reroll, False = pass
    tt[key] = max(ev_reroll, turn_score)
    return tt[key]

# True to roll, False to end turn
def positive_EV_policy(n, turn_score):
    return min(roll_EV[n-1], 10000-turn_score) - roll_F_prob[n-1]*turn_score > 0

def one_roll(n, turn_score):
    return False

def always_roll(n, turn_score):
    return True

#dice = [1]*6
#tt = {}
#print("\nExpected value of a turn using the one roll policy:")
#print(compute_over_all_rolls_policy(dice, 0, 0, one_roll, tt))

#dice = [1]*6
#tt = {}
#print("\nExpected value of a turn using the always roll policy:")
#print(compute_over_all_rolls_policy(dice, 0, 0, always_roll, tt))

#dice = [1]*6
#tt = {}
#print("\nExpected value of a turn using the positive roll EV policy:")
#print(compute_over_all_rolls_policy(dice, 0, 0, positive_EV_policy, tt))

dice = [1]*6
tt = {}
optimal_policy = {}
print("\nExpected value of a turn using the optimal policy:")
print(compute_over_all_rolls_optimal(dice, 0, 0, optimal_policy, tt))

import matplotlib.pyplot as plt

bg_color = (250/255, 245/255, 235/255)
plt.rcParams.update({
    "figure.facecolor" : bg_color,
    "axes.facecolor" : bg_color,
    "font.size" : 14,
    "ytick.labelsize" : 12,
    "figure.figsize" : (10,6)
})

for i in range(6):
    reroll = True
    for j in range(0, 10050, 50):
        key = str(i+1)+","+str(j)
        if key not in optimal_policy:
            dice = [1]*(i+1)
            ev = compute_over_all_rolls_optimal(dice, 0, j, optimal_policy, tt)
            optimal_policy[key] = ev > j
        c = 'g' if optimal_policy[key] else 'r'
        if reroll and c == 'r':
            print("For", i+1, "dice, reroll when the turn score is <=", j-50)
            reroll = False
        plt.bar(str(i+1), 50, bottom=j, color = c)

plt.xlabel("Number of dice")
plt.ylabel("Turn score")
plt.title("Optimal policy to maximize turn EV in Farkle")
ax = plt.gca()
ax.set_yticks(range(0,10500,500))
plt.grid(axis='y')
plt.savefig("farkle_optimal_policy.png")