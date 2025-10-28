import random
import math

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


def estimate_farkle_roll_EV(num_dice, num_samples=1000000):
    score_total = 0
    farkle_total = 0
    for i in range(num_samples):
        dice = [random.randint(1, 6) for _ in range(num_dice)]
        score, _ = score_dice(dice)
        score_total += score
        if score == 0:
            farkle_total += 1
    return score_total / num_samples, farkle_total / num_samples

#for i in range(1, 7):
#    print(estimate_farkle_roll_EV(i))

def random_walk(state):
    is_terminal, result = state.is_terminal()
    if is_terminal:
        return result
    moves = state.get_moves()
    rand_move = moves[random.randint(0,len(moves)-1)]
    state.make_move(rand_move)
    child_result = random_walk(state)
    state.undo_move(rand_move)
    return child_result

def random_walk_policies(state, player_policy, opponent_policy, epsilon=0):
    is_terminal, result = state.is_terminal()
    if is_terminal:
        return result
    moves = state.get_moves()
    if random.random() < epsilon:
        policy_move = random_policy(state)
    else:
        policy_move = player_policy(state)
    state.make_move(policy_move)
    child_result = random_walk_policies(state, opponent_policy, player_policy)
    state.undo_move(policy_move)
    return child_result

from tictactoe import TicTacToe

def test_matchup(p1_label, p1_policy, p2_label, p2_policy, epsilon=0):
    num_samples = 100000
    print("\nTic Tac Toe random walks results from", num_samples, "samples, epsilon", epsilon)
    for i in range(2):
        print("\nP1", p1_label, "v.s.", "P2", p2_label)
        p1_wins = 0
        p2_wins = 0
        draws = 0
        ttt = TicTacToe()
        for i in range(num_samples):
            winner = random_walk_policies(ttt, p1_policy, p2_policy, epsilon)
            if winner is None:
                draws += 1
            elif winner == 1:
                p1_wins += 1
            else:
                p2_wins += 1

        print("P1 wins:", p1_wins/num_samples, "P2 wins:", p2_wins/num_samples, "Draws:", draws/num_samples)
        tmp_policy = p2_policy
        tmp_label = p2_label
        p2_policy = p1_policy
        p2_label = p1_label
        p1_policy = tmp_policy
        p1_label = tmp_label

def random_policy(state):
    moves = state.get_moves()
    return moves[random.randint(0,len(moves)-1)]

test_matchup("Random", random_policy, "Random", random_policy)